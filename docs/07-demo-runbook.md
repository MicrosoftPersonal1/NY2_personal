# 7 · Live demo runbook – demo model (Contoso sample)

## The model
| Table | Rows | Role |
|---|---|---|
| Sales | 3,996 | Facts (order lines) |
| Customer | 1,663 | Dimension |
| Product | 2,517 | Dimension |
| Store | 74 | Dimension |
| Date | 1,826 | Date table |

Relationships: all many-to-one and single-direction, from Sales to the dimension.
- Sales[CustomerKey] → Customer[CustomerKey]
- Sales[ProductKey] → Product[ProductKey]
- Sales[StoreKey] → Store[StoreKey]
- Sales[Order Date] → Date[Date] (active)
- Sales[Delivery Date] → Date[Date] (inactive)

The test files assume these columns (standard Contoso names):
- Store[State], Store[Country]
- Product[Subcategory], Product[Category]
- Date[Month], Date[Year]
- Sales[Quantity], Sales[Net Price], Sales[Unit Cost]

Step 5 below checks them.

## Prepare (the evening before)
1. **Save as project:** in Power BI Desktop, File → Save as → Power BI project into `workspace/`, in TMDL format.
2. **Add the demo measures:**
   - TMDL view → new tab → paste `demo/setup-measures.tmdl` → Apply.
   - It creates the measures Umsatz, Kosten, Marge, Marge %, Absatz Stück and Kunden (eindeutig) in Sales.
   - Marge % is wrong on purpose: it averages the store percentages.
   - If Apply rejects the script, create the six measures by hand.
3. **Plant the relationship mistake:** Model view → relationship Sales–Customer → cross-filter direction **Both**.
4. **Report page:**
   - One matrix: Store[Country] → Store[State], with Umsatz, Marge and Marge %.
   - Write down two or three Marge % values at country level.
5. **Check the names:** press Ctrl+S in Desktop, then run Terminal → Run Task → **Tests: check catalog**.
   - Expected: "Catalogue OK" and "All KPI measures covered".
   - A missing name is listed exactly; fix it in `tests/catalog.yml` (or ask Copilot to).
6. **Fill the reference file** (demo only – in the pilot, Controlling supplies the values). With Copilot connected, ask:
   `Führe EVALUATE SUMMARIZECOLUMNS ( Store[Country], 'Date'[Year], "Value", [Umsatz] ) aus und schreibe das Ergebnis nach tests/reference/umsatz_land_jahr.csv – Kopfzeile country,year,value, Dezimalpunkt, keine Tausendertrennzeichen.`
7. **Run BPA:** run the task **BPA: check model**.
   - Expected: errors NY_MEASURE_DESCRIPTION, NY_HIDE_NUMERIC_COLUMNS and NY_USE_DIVIDE, plus warnings.
   - This also confirms that Tabular Editor reads the TMDL folder.
8. **Run all tests once:**
   - Run the task **Tests: export DAX for DAX query view**.
   - Paste `tests/generated.dax` into DAX query view and run it. You get one result per query.
   - Expected: only the **Marge %** tests at State, Category and Year return rows; the one at StoreKey returns none.
9. **Git baseline:** run `git init`, then `git add -A`, then `git commit -m "Demo baseline"`, then `git tag demo-start`.
10. **Copilot Chat:**
    - Agent mode; choose your model and keep it.
    - Power BI MCP tools enabled.
    - For the DAX query tool, choose "Allow in this session". Keep approval on for changes.
11. **Full rehearsal with a timer:**
    - Afterwards rename the branch with the result: `git branch -m feature/marge-korrektur demo-final`. That's your emergency exit.
    - Then reset (see below).
12. **Optional, if you have a TEST workspace:**
    - Run **Deploy + Test (TEST)** and take a screenshot of the PASS list.
    - Open a pull request so the pipeline checks are ready to show.

## Planted mistakes → what finds them
| Mistake | Found by |
|---|---|
| Marge % averages store percentages and uses "/" | BPA error NY_USE_DIVIDE, plus the test fails at State, Category and Year |
| Measures without description | BPA error NY_MEASURE_DESCRIPTION |
| Numeric columns visible and summed (Quantity, Net Price, Unit Cost …) | BPA error NY_HIDE_NUMERIC_COLUMNS |
| No format string or folder on the measures | BPA warnings |
| Sales–Customer filters in both directions | BPA warning NY_NO_BIDI |
| Inactive Delivery Date relationship | Not a mistake – /analyse-model explains how to use it (USERELATIONSHIP) |

## Live run (14 minutes)
| Min | Step | Do | Expected |
|---|---|---|---|
| 0–1 | Repo tour | Show `.github/copilot-instructions.md`, `.github/prompts/`, `tests/catalog.yml` | – |
| 1–2 | Connect | Paste the connect prompt (below) | Table of 5 tables, relationships, measures. "References" lists copilot-instructions.md |
| 2–4 | Analyse | Task **BPA: check model**, then `/analyse-model` | Ranked list, Marge % at the top |
| 4–6:30 | Improve | `/fix-standards` → approve → **Ctrl+S in Desktop** → Source Control diff → BPA again | Only NY_USE_DIVIDE and the warnings remain |
| 6:30–8:30 | New measure | `/new-measure name=Durchschnittspreis definition=Umsatz geteilt durch Absatz Stück` → Ctrl+S → task **Tests: check catalog** | Measure in Desktop, ratio entry in the catalogue, "covered" |
| 8:30–11:30 | Test | `/run-tests scope=Marge %` → fix prompt → `/run-tests scope=Marge %` | 3 FAIL, then 4 PASS. The matrix values change |
| 11:30–13 | Sichern | `/review-model` → new branch → commit → show the prepared pull request | No violations; checks green |
| 13–14 | AI-ready | Desktop → Prep data for AI; Copilot question on Marge % by country | The corrected value |

**Prompts:**
- Connect:
  `Verbinde dich mit '<Dateiname>' in Power BI Desktop. Liste Tabellen mit Zeilenanzahl, Beziehungen und Measures als Tabellen.`
- Fix after the failed test:
  `Analysiere, warum [Marge %] auf Store[State] fehlschlägt, und korrigiere das Measure nach unseren Standards.`
- Alternative for step 5, which shows the inactive relationship:
  `/new-measure name=Umsatz Lieferdatum definition=Umsatz nach Lieferdatum statt Bestelldatum`
  This is an additive type, tested on Date levels.

**Must show: Connect, Analyse, Improve, New measure, Test.** Sichern and AI-ready can move to slides.

## Rules during the demo
- Copilot changes the model only through MCP while Desktop is open.
- Press **Ctrl+S in Desktop** before BPA, the diff or the catalogue check – they read the files.
- No deploy or refresh live.
- No YTD or prior-year measure for /new-measure: there's no test type for it yet.

## If something goes wrong
| Problem | Do |
|---|---|
| MCP doesn't find the model | The file must be open and the name exact; restart the server (Command Palette → "MCP: List Servers") |
| Copilot is slow or goes off track | Stop it and paste the prompt again, narrower. Last resort: close Desktop, `git checkout demo-final`, reopen |
| BPA task fails | Check the Tabular Editor path in `ci/bpa.ps1`. Fallback: Desktop → External Tools → Tabular Editor → Best Practice Analyzer with `bpa/Rules-NY.json` |
| /run-tests doesn't work | Run the task **Tests: export DAX for DAX query view** and run the queries in DAX query view (0 rows = PASS) |
| No diff after Ctrl+S | Show the diff on `demo-final` |

## Reset between rehearsals
1. Close Power BI Desktop.
2. `git checkout -f main`
3. `git reset --hard demo-start`
4. `git clean -fd`
5. `git branch -D feature/marge-korrektur` (if it exists)
6. Reopen the project in Desktop.
