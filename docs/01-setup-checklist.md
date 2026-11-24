# 1 · Setup checklist

## Setup in 5 Minuten (Teil 2 Demo)
1. **VS Code + Extensions**
   - GitHub Copilot + GitHub Copilot Chat (Agent Mode)
   - Power BI Authoring MCP Server in Scout/VS Code aktiv
2. **Power BI Authoring Plugin**
   - `powerbi-authoring` aus `microsoft/skills-for-fabric` installieren.
   - Quelle: https://learn.microsoft.com/en-us/power-bi/developer/agentic/power-bi-agentic-overview
   - UNVERIFIED – bitte prüfen: exakter Installationsweg je nach VS-Code-/Copilot-Build (Marketplace vs. Skills-Import) kann variieren.
3. **Python Abhängigkeiten**
   - `pip install pyyaml requests azure-identity jsonschema fabric-cicd`
4. **Tabular Editor 2**
   - Installation prüfen; optional `TE_PATH` setzen.
   - `ci/bpa.ps1` erkennt TE2 automatisch.
5. **Power BI Desktop**
   - Preview-Feature für PBIP/PBIR aktivieren (falls noch nicht aktiv).
   - Report als PBIP speichern, damit `.Report/definition/pages/...` als Einzeldateien vorliegen.
6. **Quick Check**
   - `python ci/run_tests.py --help`
   - `pwsh -File ci/bpa.ps1` (soll starten; ohne Modell ggf. nur Hinweis)

## Prerequisites to agree with New Yorker
- [ ] Git repo (Azure DevOps or GitHub); models saved as Power BI Project (PBIP) in TMDL format
- [ ] Service principal for the pipeline; tenant setting that allows service principals to use Fabric / Power BI APIs; access to the TEST and PROD workspaces
- [ ] Tenant setting for the semantic model query API (`executeQueries`)
- [ ] XMLA endpoint and "Allow DirectQuery connection to Power BI semantic models" (needed for composite models)
- [ ] Windows build agents – Tabular Editor 2 runs on Windows only
- [ ] GitHub Copilot licences for the developers
- [ ] An approver for PROD and a certifier for "Certified" models (admins must allow certifiers)
- [ ] With RLS: run tests with a test identity or role; check the API limits for service principals on models with RLS

## Local setup (VS Code)
1. Unzip, open the folder in VS Code with GitHub Copilot (agent mode).
2. Copy the Power BI project into `workspace/` (e.g. `Umsatz.SemanticModel`, `Umsatz Filialen.Report`).
3. `pip install fabric-cicd azure-identity requests pyyaml`, then `az login`.
   The scripts use `DefaultAzureCredential`: locally your `az login`, in the pipeline the service principal.
4. Fill the workspace IDs in `ci/deploy.py`.
5. Install Tabular Editor 2 and set its path in `ci/bpa.ps1`.
6. The test files use the names of the demo model (Sales, Customer, Product, Store, Date – Contoso sample). For a New Yorker model, change the names in `tests/` and in the "Aktuelles Modell" section of `.github/copilot-instructions.md`; the task "Tests: check catalog" lists every name that does not exist in the model.
7. Check that the standards file is active: in a Copilot answer open "References" – `copilot-instructions.md` must be listed.
8. Terminal → Run Task → "BPA: check model", "Tests: check catalog", then "Deploy + Test (TEST)".

## Azure DevOps setup
1. Library → variable group `ny-fabric`: `TENANT_ID`, `CLIENT_ID`, `CLIENT_SECRET` (secret), `TEST_WS_ID`, `TEST_DS_ID`, `PROD_WS_ID`.
2. Pipelines → new pipeline from `azure-pipelines.yml`.
3. Pipelines → Environments → `ny-bi-prod` → Approvals and checks → add the approver (e.g. Tilo).
4. Repos → Branches → main → Branch policies:

| Policy | Setting |
|---|---|
| Minimum number of reviewers | 1 – for core models 2 |
| Automatically included reviewers | Path `/workspace/*.SemanticModel/*` → group "BI Architecture" |
| Comment resolution | Required |
| Build validation | This pipeline, required |
| Linked work items | Optional, recommended |

PR validation in Azure Repos comes from the branch policy (Build validation), not from a `pr:` section in the YAML.
GitHub instead: branch ruleset, CODEOWNERS file and required status checks; use `-G` instead of `-V` for the BPA output.

## Rolling out the BPA rules
- First run on an existing model: set all rules to severity 2 – full list, nobody blocked.
- Let Copilot fix the findings: "Fix all severity 3 violations from the bpa-*.txt files. Only change descriptions, formats and folders – never DAX logic."
- Then raise the important rules to severity 3 (blocks the pull request).
- Also enable "Discourage implicit measures" in the model properties (depending on the Tabular Editor version as a model rule, otherwise on the review checklist).

## Before the demo / first real use
- The scripts and config files load without errors, but have **not** been run against a real model yet – do one dry run on a test model.
- All table, column, measure and workspace names are placeholders.
- `tests/reference/umsatz_land_jahr.csv` has no values yet – the reference check fails until it has rows (demo: see docs/07; pilot: Controlling supplies them).
- The enhanced refresh call (`type: full`) in `ci/refresh.py` needs Premium or Fabric capacity.
