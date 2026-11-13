# AI-ready semantic model – starter repo (New Yorker pilot)

Starter files from the technical appendix, **set up for the demo model** (Contoso sample data:
Sales, Customer, Product, Store, Date). For a New Yorker model, change the names in `tests/` and in the
"Aktuelles Modell" section of `.github/copilot-instructions.md` – the task "Tests: check catalog" lists every
name that does not exist in the model. Not yet tested against a real model.

**Live demo: start with `docs/07-demo-runbook.md`. Pilot setup: `docs/01-setup-checklist.md`.**

## Quick start
1. Open this folder in VS Code (GitHub Copilot, agent mode, Power BI MCP extension).
2. Save the model as a Power BI project (PBIP, TMDL format) into `workspace/`.
3. `pip install fabric-cicd azure-identity requests pyyaml` and `az login`.
4. Fill the workspace IDs in `ci/deploy.py`; install Tabular Editor 2 at the path in `ci/bpa.ps1`.
5. Terminal > Run Task: "BPA: check model", "Tests: check catalog", "Deploy + Test (TEST)".

## Copilot chat commands (`.github/prompts/`)
| Command | What it does |
|---|---|
| /analyse-model | Improvement potential of the connected model, ranked – changes nothing |
| /fix-standards | Fixes severity-3 BPA findings that need no DAX change (descriptions, hidden columns, formats, folders) |
| /new-measure | New KPI measure with description, format, folder – plus its entry in tests/catalog.yml |
| /run-tests | Runs the catalogue tests against the connected model (0 rows = PASS) |
| /review-model | Checks uncommitted changes against the standards – changes nothing |

## VS Code tasks (Terminal > Run Task)
| Task | What it does | Needs |
|---|---|---|
| BPA: check model | Best Practice Analyzer with bpa/Rules-NY.json | Tabular Editor 2, saved model |
| Tests: check catalog | Catalogue names exist in the model + every KPI measure has a test | Saved model |
| Tests: export DAX for DAX query view | Writes all test queries to tests/generated.dax | – |
| Deploy + Test (TEST) | Deploy to TEST, refresh, run all tests | az login, TEST workspace |

## Contents
| Path | Purpose |
|---|---|
| docs/01-setup-checklist.md | Prerequisites, local + Azure DevOps setup, branch policies, BPA rollout, caveats |
| docs/02-release-gate.md | What runs when, the release gate, Fabric deployment pipelines, reference values |
| docs/03-when-a-test-fails.md | Symptoms, causes and the Copilot prompt for fixing |
| docs/04-core-models-and-composite.md | Core models, workspaces, thin reports, composite steps, limits, governance |
| docs/05-pilot-plan.md | Mapping to the 4-week pilot |
| docs/06-options-for-later.md | Fabric notebook tests, Semantic Link Labs BPA, new Tabular Editor CLI |
| docs/07-demo-runbook.md | Live demo on the demo model: preparation, planted mistakes, 14-minute run sheet, fallbacks |
| demo/setup-measures.tmdl | Demo measures for TMDL view (Marge % deliberately wrong) |
| .github/copilot-instructions.md | Standards Copilot always follows, incl. the current model |
| .github/instructions/*.instructions.md | Rules for TMDL files and tests (applyTo) |
| .github/prompts/*.prompt.md | The five chat commands above |
| .azuredevops/pull_request_template.md | PR checklist |
| .vscode/tasks.json | The VS Code tasks above |
| bpa/Rules-NY.json | 8 Best Practice Analyzer rules |
| ci/bpa.ps1 | Run BPA locally (Windows) |
| ci/deploy.py, refresh.py, run_tests.py, deploy_and_test.py | Deploy to TEST, refresh, aggregation tests (`run_tests.py --print-dax` works without the service) |
| ci/check_test_coverage.py | Fails if a KPI measure has no test |
| ci/check_catalog_names.py | Fails if the catalogue names a table, column or measure the model does not have |
| ci/check_shared_dimensions.py | Fails if shared dimensions differ between core models |
| tests/catalog.yml | Which measure is tested how, on which levels |
| tests/reference/umsatz_land_jahr.csv | Approved reference values (empty – fill before use) |
| tests/dax/*.dax | Manual DAX test queries A, A2, B, C for DAX query view |
| notebooks/measure_tests_fabric.py | Same tests as a Fabric notebook (Semantic Link) |
| azure-pipelines.yml | Validate / DeployTest / DeployProd |
