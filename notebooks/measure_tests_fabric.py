# Fabric notebook: measure tests with Semantic Link (sempy is preinstalled in Fabric notebooks)
# Names match the demo model (Contoso sample: Sales, Customer, Product, Store, Date).
# Paste the DAX from tests/dax/*.dax into the placeholders – or all queries from
# `python ci/run_tests.py --print-dax tests/generated.dax`.
import sempy.fabric as fabric
import pandas as pd

DATASET   = "<semantic model name>"   # your semantic model
WORKSPACE = "<test workspace name>"   # test workspace
TOL       = 0.01                      # tolerance for rounding

tests = {
    "Umsatz: stores = state":       """<query A>""",
    "Umsatz: countries = total":    """<query A2>""",
    "Marge %: ratio by state":      """<query B>""",
}

results = []
for name, dax in tests.items():
    df = fabric.evaluate_dax(DATASET, dax, workspace=WORKSPACE)
    diff = df[[c for c in df.columns if "Diff" in c][0]].fillna(0)
    bad = df[diff.abs() > TOL]
    results.append({"test": name, "rows": len(df),
                    "failed_rows": len(bad), "passed": bad.empty})

# Distinct customers: largest store <= country <= sum of stores (query C returns column "Ok")
df = fabric.evaluate_dax(DATASET, """<query C>""", workspace=WORKSPACE)
bad = df[~df[[c for c in df.columns if c.endswith("[Ok]") or c == "Ok"][0]].astype(bool)]
results.append({"test": "Kunden (eindeutig): range by country", "rows": len(df),
                "failed_rows": len(bad), "passed": bad.empty})

# Reference check: model vs. source table in the lakehouse (table and column names are placeholders)
model = fabric.evaluate_dax(DATASET, """
EVALUATE SUMMARIZECOLUMNS ( Store[Country], 'Date'[Year], "Umsatz", [Umsatz] )
""", workspace=WORKSPACE)
model.columns = ["country", "year", "model_umsatz"]

source = spark.sql("""
    SELECT st.Country AS country, YEAR(s.OrderDate) AS year,
           SUM(s.Quantity * s.NetPrice) AS source_umsatz
    FROM sales s JOIN store st ON s.StoreKey = st.StoreKey
    GROUP BY st.Country, YEAR(s.OrderDate)
""").toPandas()

cmp = model.merge(source, on=["country", "year"], how="outer").fillna(0)
cmp["diff"] = cmp["model_umsatz"] - cmp["source_umsatz"]
bad = cmp[cmp["diff"].abs() > TOL]
results.append({"test": "Umsatz vs. source", "rows": len(cmp),
                "failed_rows": len(bad), "passed": bad.empty})

res = pd.DataFrame(results).assign(run_ts=pd.Timestamp.now())
display(res)
spark.createDataFrame(res).write.mode("append").saveAsTable("measure_test_results")

assert res["passed"].all(), "Measure tests failed – model not approved"
