"""Aggregation tests generated from tests/catalog.yml.

Against a published model (pipeline, or the "Deploy + Test (TEST)" task):
    python ci/run_tests.py --ws <workspace-id> --ds <dataset-id> [--junit test-results.xml]
Without the service – write all queries to one file for DAX query view or for Copilot (/run-tests):
    python ci/run_tests.py --print-dax tests/generated.dax [--only "Marge %,Umsatz"]
"""
import argparse, csv, sys, yaml
from xml.etree.ElementTree import Element, SubElement, ElementTree

T_ADD = """EVALUATE
VAR t = SUMMARIZECOLUMNS ( {parent}, "Parent", [{m}],
    "SumChildren", SUMX ( VALUES ( {child} ), [{m}] ) )
RETURN FILTER ( ADDCOLUMNS ( t, "Diff", [Parent] - [SumChildren] ), ABS ( [Diff] ) > {tol} )"""
T_TOTAL = """EVALUATE
VAR tot = CALCULATE ( [{m}], REMOVEFILTERS () )
VAR parts = SUMX ( ALLNOBLANKROW ( {top} ), [{m}] )
RETURN FILTER ( ROW ( "Total", tot, "SumParts", parts, "Diff", tot - parts ), ABS ( [Diff] ) > {tol} )"""
T_RATIO = """EVALUATE
VAR t = SUMMARIZECOLUMNS ( {level}, "Value", [{m}], "Expected", DIVIDE ( [{num}], [{den}] ) )
RETURN FILTER ( ADDCOLUMNS ( t, "Diff", [Value] - [Expected] ), ABS ( [Diff] ) > {tol} )"""
T_SEMI = """EVALUATE
VAR t = SUMMARIZECOLUMNS ( {period}, "Value", [{m}],
    "Expected", CALCULATE ( [{m}], LASTNONBLANK ( 'Date'[Date], CALCULATE ( COUNTROWS ( {fact} ) ) ) ) )
RETURN FILTER ( ADDCOLUMNS ( t, "Diff", [Value] - [Expected] ), ABS ( [Diff] ) > {tol} )"""
T_DIST = """EVALUATE
VAR t = SUMMARIZECOLUMNS ( {parent}, "Value", [{m}],
    "MaxChild", MAXX ( VALUES ( {child} ), [{m}] ), "SumChildren", SUMX ( VALUES ( {child} ), [{m}] ) )
RETURN FILTER ( t, [Value] < [MaxChild] || [Value] > [SumChildren] )"""
T_DATA = """EVALUATE ROW ( "Value", [{m}] )"""


def generate(t, tol):
    m, typ = t["measure"], t["type"]
    if typ == "additive":
        for parent, child in t["paths"]:
            yield (f"{m}: {child} -> {parent}",
                   T_ADD.format(m=m, parent=parent, child=child, tol=tol["amount"]))
        if "total" in t:
            yield (f"{m}: {t['total']} -> total",
                   T_TOTAL.format(m=m, top=t["total"], tol=tol["amount"]))
    elif typ == "ratio":
        for lvl in t["levels"]:
            yield (f"{m}: ratio at {lvl}",
                   T_RATIO.format(m=m, level=lvl, num=t["numerator"], den=t["denominator"],
                                  tol=tol["ratio"]))
    elif typ == "semi_additive":
        for p in t["periods"]:
            yield (f"{m}: last value per {p}",
                   T_SEMI.format(m=m, period=p, fact=t["fact"], tol=tol["amount"]))
    elif typ == "distinct":
        for parent, child in t["paths"]:
            yield (f"{m}: distinct {child} -> {parent}",
                   T_DIST.format(m=m, parent=parent, child=child))
    else:
        raise ValueError(f"{m}: unknown type '{typ}'")


def ref_query(ref):
    return f'EVALUATE SUMMARIZECOLUMNS ( {", ".join(ref["by"])}, "Value", [{ref["measure"]}] )'


def load_reference(path):
    with open(path, encoding="utf-8") as f:
        rd = csv.reader(f)
        next(rd, None)
        return {tuple(r[:-1]): float(r[-1]) for r in rd if r}


def print_dax(cat, tol, only, path):
    out = ["// Aggregation tests generated from tests/catalog.yml",
           "// Paste into DAX query view (one result per EVALUATE) or let Copilot run them (/run-tests).", ""]
    if cat.get("data_check") and (not only or cat["data_check"] in only):
        out += [f"// [value must not be blank] {cat['data_check']}: model has data",
                T_DATA.format(m=cat["data_check"]), ""]
    for t in cat["tests"]:
        if only and t["measure"] not in only:
            continue
        for name, dax in generate(t, tol):
            out += [f"// [0 rows = PASS] {name}", dax, ""]
    for ref in cat.get("reference", []):
        if only and ref["measure"] not in only:
            continue
        out += [f"// [compare with {ref['file']}] {ref['measure']}: vs reference", ref_query(ref), ""]
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    print(f"{sum(1 for l in out if l.startswith('EVALUATE'))} queries written to {path}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ws")
    ap.add_argument("--ds")
    ap.add_argument("--catalog", default="tests/catalog.yml")
    ap.add_argument("--junit", default="test-results.xml")
    ap.add_argument("--print-dax", metavar="FILE", help="only write the queries to FILE, no service needed")
    # argparse %-formatting requires escaping a literal percent as %%
    ap.add_argument("--only", help="comma-separated measure names, e.g. \"Marge %%,Umsatz\"")
    a = ap.parse_args()

    cat = yaml.safe_load(open(a.catalog, encoding="utf-8"))
    tol = cat.get("tolerance", {"amount": 0.01, "ratio": 0.0001})
    only = {s.strip() for s in a.only.split(",")} if a.only else None

    if a.print_dax:
        print_dax(cat, tol, only, a.print_dax)
        return
    if not (a.ws and a.ds):
        ap.error("--ws and --ds are required (or use --print-dax)")

    import requests
    from azure.identity import DefaultAzureCredential
    tok = DefaultAzureCredential().get_token("https://analysis.windows.net/powerbi/api/.default").token
    url = f"https://api.powerbi.com/v1.0/myorg/groups/{a.ws}/datasets/{a.ds}/executeQueries"
    hdr = {"Authorization": f"Bearer {tok}"}

    def run(dax):
        payload = {"queries": [{"query": dax}], "serializerSettings": {"includeNulls": True}}
        r = requests.post(url, headers=hdr, json=payload)
        is_json = r.headers.get("content-type", "").startswith("application/json")
        body = r.json() if is_json else {}
        if r.status_code != 200 or "error" in body:
            return None, (body.get("error") or r.text)
        res = body["results"][0]
        if "error" in res:
            return None, res["error"]
        return res["tables"][0]["rows"], None

    results = []

    if cat.get("data_check") and (not only or cat["data_check"] in only):
        m = cat["data_check"]
        rows, err = run(T_DATA.format(m=m))
        val = list(rows[0].values())[0] if rows else None
        ok = not err and val not in (None, 0)
        results.append((m, f"{m}: model has data", ok, "" if ok else (f"Query error: {err}" if err else "value is blank or 0")))

    for t in cat["tests"]:
        if only and t["measure"] not in only:
            continue
        for name, dax in generate(t, tol):
            rows, err = run(dax)
            if err:
                results.append((t["measure"], name, False, f"Query error: {err}"))
            elif rows:
                results.append((t["measure"], name, False, f"{len(rows)} rows off, e.g. {rows[:3]}"))
            else:
                results.append((t["measure"], name, True, ""))

    for ref in cat.get("reference", []):
        if only and ref["measure"] not in only:
            continue
        name = f'{ref["measure"]}: vs reference {ref["file"]}'
        gold = load_reference(ref["file"])
        if not gold:
            results.append((ref["measure"], name, False, "reference file has no rows – add the approved values"))
            continue
        rows, err = run(ref_query(ref))
        if err:
            results.append((ref["measure"], name, False, f"Query error: {err}"))
            continue
        model = {tuple(str(v) for v in list(r.values())[:-1]): (list(r.values())[-1] or 0) for r in rows}
        bad = [(k, model.get(k, 0), v) for k, v in gold.items() if abs(model.get(k, 0) - v) > tol["amount"]]
        results.append((ref["measure"], name, not bad, f"{len(bad)} keys off, e.g. {bad[:3]}" if bad else ""))

    suite = Element("testsuite", name="Aggregation check", tests=str(len(results)),
                    failures=str(sum(1 for r in results if not r[2])))
    for measure, name, ok, msg in results:
        print(("PASS " if ok else "FAIL ") + name + ("" if ok else f"  -> {msg}"))
        tc = SubElement(suite, "testcase", classname=measure, name=name)
        if not ok:
            SubElement(tc, "failure", message=msg[:200]).text = msg
    ElementTree(suite).write(a.junit, encoding="utf-8", xml_declaration=True)
    sys.exit(0 if all(r[2] for r in results) else 1)


if __name__ == "__main__":
    main()
