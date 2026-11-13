# 2 · What runs when, and the release gate

| Check | Needs data? | When | Finds |
|---|---|---|---|
| Best Practice Analyzer (BPA) | No – reads only the model files | Locally and on every pull request | Missing descriptions, implicit measures, `/` instead of DIVIDE, bi-directional relationships, naming errors |
| Coverage check | No | Every pull request | New KPI without a test |
| DAX tests / aggregation check | Yes | After deploy to TEST and refresh | Wrong numbers across levels, deviations from reference values |

## The gate
1. **Merge to main** → deploy to TEST, then refresh.
2. **Aggregation check** → if a test fails: stop. PROD stays untouched.
3. **Approval** on environment `ny-bi-prod` (e.g. Tilo).
4. **PROD & Copilot** → the owner sets "Approved for Copilot" (and "Certified" where applicable).

Output: PASS/FAIL per test in the console, a JUnit file shown in the "Tests" tab of each run (with history), exit code 1 stops the pipeline before PROD.

## With Fabric deployment pipelines
Git → DEV workspace stays as it is. Azure DevOps tests the TEST stage and triggers TEST → PROD only after green tests, via the deployment pipeline REST API.

## Reference values
- Controlling supplies them from the ERP (`tests/reference/*.csv`).
- Closed months only – they no longer change.
- Update once a month via pull request.
