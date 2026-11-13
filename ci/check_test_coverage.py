import glob, re, sys, yaml

catalog = yaml.safe_load(open("tests/catalog.yml", encoding="utf-8"))
tested = {t["measure"] for t in catalog["tests"]}
missing, current = [], None
for f in glob.glob("workspace/**/definition/tables/*.tmdl", recursive=True):
    for line in open(f, encoding="utf-8"):
        m = re.match(r"\tmeasure\s+('(?:[^']|'')+'|[^\s=]+)\s*=", line)
        if m:
            current = m.group(1).strip("'").replace("''", "'")
            continue
        d = re.match(r"\t\tdisplayFolder:\s*(.+)", line)
        if current and d:
            if d.group(1).strip().startswith("KPI") and current not in tested:
                missing.append(current)
            current = None
if missing:
    print("KPI measures without a test:", ", ".join(sorted(set(missing))))
    sys.exit(1)
print("All KPI measures covered.")
