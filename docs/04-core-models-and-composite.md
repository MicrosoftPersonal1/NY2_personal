# 4 · Shared core models and composite models

## Core models
| Core model | Content | Shared dimensions |
|---|---|---|
| Umsatz & Marge | Sales, returns, margin, promotions | Date, Store, Article, Country |
| Bestand & Warenfluss | Stock, deliveries, distribution | Date, Store, Article, Warehouse |
| Einkauf | Orders, suppliers, delivery delays | Date, Article, Supplier |

**Rule:** shared dimensions (Date, Store, Article) are identical in every core model – same names, hierarchies and descriptions.
Copy them as TMDL files from a template folder; `ci/check_shared_dimensions.py` checks they stay identical. This also prepares the later Fabric IQ ontology.

## Workspaces, permissions, storage mode
- **NY Core – DEV / TEST / PROD:** core models only. Owner: BI team. PROD only via the pipeline.
- **NY Reports – <area>:** thin reports and extensions from the business areas.
- **NY Apps:** distribution to end users.
- Build permission for an Entra group "BI Report Authors" on the PROD core models; read access via app or workspace.
- Mark PROD core models "Certified", discoverable in the OneLake catalog, "Approved for Copilot".
- Storage mode with Snowflake in mind: Import or Direct Lake via mirroring – all queries (Copilot and extensions too) hit Power BI, not Snowflake, and cost no Snowflake credits.

## Thin reports (no own model)
1. Power BI Desktop → Get data → Power BI semantic models → pick the core model (live connection).
2. Build the report and save as Power BI project – the folder contains only the report.
3. Report measures for layout only. Real KPIs belong in the core model.

## Extending with a composite model – example: store-cluster targets from Excel
1. Connect live to the core model.
2. Choose "Make changes to this model": the live connection becomes DirectQuery with a local model.
3. Select only the tables needed, e.g. Store, Date, Sales.
4. Get data → Excel → import table "Filialcluster-Ziele".
5. Create relationship Ziele[StoreKey] → Store[StoreKey] (will be "limited").
6. Local measures, e.g. `Zielerreichung % = DIVIDE ( [Umsatz], [Ziel] )`.
7. Publish to the area workspace – not the core workspace.

## Limits you need to know
| Topic | What applies |
|---|---|
| Tenant settings | "Allow XMLA Endpoints and Analyze in Excel with on-premises semantic models" and "Allow DirectQuery connection to Power BI semantic models" must be on |
| Permissions | The composite model owner needs Build permission on the source models |
| Chain length | Max three models in a chain. NY rule: core model → one extension, no more |
| Security (RLS) | RLS only applies in the model where it is defined. Local Excel tables are not protected |
| Data access | Users of a report on an extension can query all tables of the source model not protected by RLS |
| Relationships | Cross-source always "limited". Join columns ideally ≤ 50,000 values – Store and Category yes, article number no |
| Calculation groups | Not supported on remote sources – results undefined |
| Automation | Remote models via single sign-on only; service principal not supported. Chains can be prevented with "Discourage chaining" |

Source: Microsoft Learn – "Use composite models in Power BI Desktop".

## Governance
1. **Bring back:** when more than one team uses an extension or it becomes business-critical, move its tables and measures into the core model via pull request with tests.
2. **No breaking changes without notice:** don't rename or delete measures at once – hide them, description "Veraltet – ersetzt durch [X]", remove after 2 releases.
3. **Check impact before core changes:** lineage view / impact analysis in the Fabric workspace shows dependent reports and extensions.
4. **AI only on core models:** Copilot, data agents and later Fabric IQ use only certified core models with "Approved for Copilot". Extensions are for reports, not AI.

Option in Fabric: a Direct Lake core model – the import addition goes into the same model instead of a separate one (Import and Direct Lake tables combined in web modelling).
