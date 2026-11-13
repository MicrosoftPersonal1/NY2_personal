---
name: 'Aggregation tests'
description: 'Use when adding or changing entries in tests/catalog.yml.'
applyTo: 'tests/**'
---
- Every KPI measure (displayFolder starts with "KPI") has an entry in tests/catalog.yml.
- Choose the type from the business meaning, in this order (first match wins):
  1. Counts unique things (customers, orders) → `distinct`
  2. A ÷ B (a %, a value per unit, an average) → `ratio`, with `numerator` and `denominator` measures
  3. A level at a point in time (stock, open orders) → `semi_additive`, with `fact` and `periods`
  4. Year-to-date, prior year, change vs. prior year → no template yet: do not add a test, flag it in the PR summary
  5. Otherwise → `additive`
- Use only levels that exist in this model:
  - Store: `Store[StoreKey]` → `Store[State]` → `Store[Country]`
  - Product: `Product[ProductKey]` → `Product[Subcategory]` → `Product[Category]`
  - Date: `'Date'[Month]` → `'Date'[Year]`
- additive: one `[parent, child]` pair per step; add `total: "Store[Country]"` for the main KPI.
- ratio: the lowest level (`Store[StoreKey]`) plus every level reports or the agent use.
- distinct: `[parent, child]` pairs; the check is "largest child ≤ parent ≤ sum of children".
- Write columns as `Table[Column]`, always quote `'Date'`. Measure names exactly as in the model.
- After editing run the task "Tests: check catalog" (names exist in the model, every KPI has a test).
