# 8 · AI-Pull-Request-Review einrichten (GitHub + Azure Repos)

Zielbild: **KI prüft und kommentiert, Menschen entscheiden und mergen.**

## GitHub (Copilot Code Review)
Quelle: https://docs.github.com/en/copilot/how-tos/copilot-on-github/set-up-copilot/configure-code-review

1. Repository öffnen → **Settings** → **Rules** → **Rulesets**.
2. Neues Branch-Ruleset für `main` anlegen oder bestehendes anpassen.
3. Unter Pull-Request-Regeln aktivieren:
   - **Require a pull request before merging**
   - **Require approvals** = mindestens 1 menschliche Freigabe
   - **Require status checks to pass** (mindestens `PR Quality / BPA`, `PR Quality / PBIR JSON Schema`, `PR Quality / DAX Tests or DAX Export`)
4. In den Copilot-Einstellungen für das Repository **Automatically request Copilot code review** aktivieren.
5. In `.github/copilot-instructions.md` den Abschnitt „Code Review“ pflegen (repo-spezifische Regeln).

> UNVERIFIED – bitte prüfen: Die genaue Platzierung des Schalters „Automatically request Copilot code review“ kann je nach GitHub-Plan/UI leicht variieren.

## Azure Repos (Copilot Code Review)
Quelle: https://learn.microsoft.com/en-us/azure/devops/repos/git/copilot-code-reviews?view=azure-devops

1. Auf Organisationsebene Copilot Code Review aktivieren.
2. Im Projekt und im Ziel-Repository Copilot Code Review freischalten.
3. Branch-Policy für `main` setzen:
   - PR erforderlich
   - mindestens 1 menschlicher Reviewer
   - Build-Validierung mit `azure-pipelines/pr-quality.yml`
   - automatische Review-Anforderung aktivieren (falls als Option verfügbar)
4. Repo-spezifische Review-Instruktionen hinterlegen (DAX/TMDL/PBIR-Regeln aus `.github/copilot-instructions.md` übernehmen).
5. Mit einem Test-PR verifizieren, dass Copilot-Kommentare erzeugt werden und die Pipeline-Checks laufen.

> UNVERIFIED – bitte prüfen: Die Menübezeichnungen unterscheiden sich zwischen Azure DevOps Services/Tenant-Rollout-Ständen.

## Benötigte Secrets / Variablen

### GitHub Actions (Repository Secrets)
- `AZURE_TENANT_ID`
- `AZURE_CLIENT_ID`
- `AZURE_CLIENT_SECRET`
- `TEST_WS_ID`
- `TEST_DS_ID`

Wenn diese fehlen, läuft der Fallback: `run_tests.py --print-dax` + Artifact `generated.dax`.

### Azure Pipelines (Variable Group oder Pipeline-Variablen)
- `TENANT_ID`
- `CLIENT_ID`
- `CLIENT_SECRET` (secret)
- `TEST_WS_ID`
- `TEST_DS_ID`

## Grenzen (für den Kundentermin explizit sagen)
1. AI-Reviews sind **nicht deterministisch**; zwei Läufe können leicht unterschiedliche Hinweise geben.
2. AI-Review **approvt nicht** und **blockiert nicht** selbstständig den Merge.
3. Fachliche Freigabe der Kennzahlen bleibt bei **Controlling/BI-Verantwortlichen**.
4. AI erhält **keine Deploy-Credentials**; Deployments laufen nur über gesicherte Pipeline-Identitäten.
