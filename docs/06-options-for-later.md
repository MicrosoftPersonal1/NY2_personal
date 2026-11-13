# 6 · Options for later

- **Tests in a Fabric notebook instead of the pipeline:** `notebooks/measure_tests_fabric.py` runs the same DAX tests with Semantic Link, compares with the source tables, writes the results to a Delta table (history for a small Power BI report) and fails on errors – can be scheduled after the nightly refresh in a Fabric Data Pipeline.
- **BPA across all models (ops team):** Semantic Link Labs has a built-in BPA function in Fabric notebooks – run nightly over all models and show the results in a report.
- **New Tabular Editor CLI ("te"):** cross-platform, with built-in DAX assertion tests. Was in limited preview until 31.10.2026 – check the current status before use.
