"""Checks that every table, column and measure named in tests/catalog.yml exists in the model.

Reads the TMDL files under workspace/ (save in Power BI Desktop first). No service and no sign-in needed.
Exit code 1 lists every name that is missing, so a renamed column or measure is caught before the tests run.
"""
import glob, os, re, sys, yaml

NAME = r"('(?:[^']|'')+'|[^\s=']+)"
RE_TABLE = re.compile(r"^table\s+" + NAME)
RE_COLUMN = re.compile(r"^\tcolumn\s+" + NAME)
RE_MEASURE = re.compile(r"^\tmeasure\s+" + NAME)
RE_COLREF = re.compile(r"(?:'((?:[^']|'')+)'|([^\s,'\[\]]+))\[([^\]]+)\]")


def unquote(n):
    return n[1:-1].replace("''", "'") if n.startswith("'") else n


def key(n):
    return n.strip().casefold()


tables, columns, measures = set(), set(), set()
files = glob.glob("workspace/**/definition/tables/*.tmdl", recursive=True)
for f in files:
    table = None
    for line in open(f, encoding="utf-8-sig"):
        line = line.rstrip("\n")
        if m := RE_TABLE.match(line):
            table = unquote(m.group(1))
            tables.add(key(table))
        elif table and (m := RE_COLUMN.match(line)):
            columns.add((key(table), key(unquote(m.group(1)))))
        elif m := RE_MEASURE.match(line):
            measures.add(key(unquote(m.group(1))))

if not files:
    print("No TMDL model found under workspace/ – save the model as a Power BI project (TMDL) first.")
    sys.exit(1)

cat = yaml.safe_load(open("tests/catalog.yml", encoding="utf-8"))
missing = []


def need_measure(name, where):
    if name and key(name) not in measures:
        missing.append(f"measure [{name}]  (used in {where})")


def need_columns(text, where):
    refs = RE_COLREF.findall(text or "")
    if text and not refs:
        missing.append(f"'{text}' is not written as Table[Column]  (used in {where})")
    for quoted, plain, col in refs:
        t = quoted.replace("''", "'") if quoted else plain
        if key(t) not in tables:
            missing.append(f"table '{t}'  (used in {where})")
        elif (key(t), key(col)) not in columns:
            missing.append(f"column '{t}'[{col}]  (used in {where})")


need_measure(cat.get("data_check"), "data_check")
for t in cat.get("tests", []):
    m = t.get("measure")
    need_measure(m, m)
    need_measure(t.get("numerator"), f"{m} numerator")
    need_measure(t.get("denominator"), f"{m} denominator")
    for pair in t.get("paths", []):
        for c in pair:
            need_columns(c, f"{m} paths")
    for c in t.get("levels", []) + t.get("periods", []):
        need_columns(c, f"{m} levels")
    if t.get("total"):
        need_columns(t["total"], f"{m} total")
    if t.get("fact") and key(t["fact"]) not in tables:
        missing.append(f"table '{t['fact']}'  (used in {m} fact)")
for r in cat.get("reference", []):
    need_measure(r.get("measure"), "reference")
    for c in r.get("by", []):
        need_columns(c, "reference")
    if not os.path.exists(r.get("file", "")):
        missing.append(f"file {r.get('file')}  (reference)")

if missing:
    print("Catalogue names not found in the model:")
    for x in dict.fromkeys(missing):
        print("  -", x)
    sys.exit(1)
print(f"Catalogue OK: all names exist in the model ({len(tables)} tables, {len(measures)} measures read).")
