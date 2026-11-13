# 3 · When a test fails

| Symptom | Typical cause |
|---|---|
| Additive: children ≠ parent | Bi-directional relationship, many-to-many, or a filter in the measure (ALL in the wrong place) |
| Total ≠ sum of countries | Sales rows whose StoreKey is missing in the Store table (orphans) – fix the load process |
| Ratio ≠ numerator ÷ denominator | The measure averages percentages or uses its own SUMs instead of the base measures |
| Stock: month ≠ last day | Measure uses SUM instead of LASTNONBLANK / LASTDATE |
| Distinct: total > sum | Error in the many-to-many or currency logic |
| Deviation from reference | Returns or VAT logic differs from the Finance definition – clarify the business rule |

"Last day" for stock is New Yorker's business rule: last calendar day or last day with stock data.

**Tip:** paste the failed test into Copilot chat:
> Analyse why [Marge %] fails on Store[State] and propose a fix that follows our standards.
