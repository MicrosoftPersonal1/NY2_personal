# 9 · Demo-Runbook Teil 2 (45 Min)

Termin: **Di, 01.12.2026, 10:30 CET**  
Kunde: **New Yorker (BI-Team)**

## 0) Vor dem Termin (5 Minuten)
1. Branch `demo/teil2-prep` öffnen.
2. Power BI Desktop mit `ContosoDemo10k` geöffnet lassen.
3. In VS Code prüfen:
   - Copilot Agent Mode aktiv
   - Power BI Authoring MCP verbunden
4. Optional Backup-Branch lokal verfügbar: `feature/report-umsatz-land`.

## 1) Ablauf im Termin (minute-by-minute)

| Minute | Abschnitt | Was ich sage / tue | Was das Publikum sieht | Fallback |
|---|---|---|---|---|
| 0–3 | Einstieg | Zielbild: „KI unterstützt Entwicklung und Review, aber Menschen entscheiden.“ | Agenda mit 3 Blöcken | Vorbereitete Folie statt Live-Einstieg |
| 3–6 | Repo-Überblick | Zeige `.github/instructions`, `.github/prompts`, `ci/`, `docs/` | Governance im Repo, keine Blackbox | Screenshots der Struktur |
| 6–15 | **Teil A**: Report-Entwicklung mit KI | Nutze Prompt „Neue Seite bauen“ (siehe unten) | Neue Seite mit KPI/Karten/Diagrammen/Slicer | Backup-Seite aus `feature/report-umsatz-land` zeigen |
| 15–21 | **Teil A**: Qualitätsreview | Nutze Prompt `/review-report` | Tabelle mit Verstößen für „Umsatz Übersicht (alt)“ | Vorbereiteter Review-Output in Folie |
| 21–28 | **Teil B**: PR + Quality Gates | Zeige PR-Workflow Dateien (`.github/workflows/pr-quality.yml`, `azure-pipelines/pr-quality.yml`) | KI-Review + BPA + Tests + PBIR-Schema als Checks | Nur YAML-Snippets auf Folie |
| 28–34 | **Teil B**: AI-Reviewer-Fund | Zeige geplanten PR-Diff mit „Umsatz pro Filiale“ (mit `/` statt `DIVIDE`, ohne Beschreibung) | Konkreter KI-Hinweis + menschliche Entscheidung | Vorbereiteter Screenshot vom Kommentar |
| 34–41 | **Teil C**: Betriebsfähigkeit | Zeige `docs/08` (Setup), `docs/01` (5-Min-Setup), `scripts/reset-demo.ps1` | Wiederholbare Demo + klare Grenzen | Nur Runbook zeigen |
| 41–45 | Abschluss | „KI prüft und kommentiert, Menschen entscheiden und mergen.“ | Klare Governance-Botschaft | Q&A |

## 2) Exakte Prompts für den Live-Teil

### 2.1 Broken-Page Review (live)
```text
/review-report
Bitte prüfe alle Report-Seiten gegen .github/instructions/report-standards.instructions.md
und gib nur die Tabelle aus: Seite | Visual | Regel | Befund | Vorschlag.
```

### 2.2 Neue saubere Seite bauen (A8 – vorbereitet, nicht jetzt ausführen)
```text
/new-report-page
Seitenname: Umsatz & Marge je Land
Businessfrage: Wie entwickeln sich Umsatz und Marge nach Land und Monat im Jahr 2025?

Baue eine Seite mit:
- KPI-Karten: Umsatz, Marge, Marge %
- Balkendiagramm: Umsatz nach Country
- Säulendiagramm: Umsatz nach Month
- Slicer: Year

Nutze ausschließlich bestehende explizite Measures aus dem Modell,
wende das Theme themes/ny-ibcs-demo.json an
und führe danach einen Selbstcheck gegen report-standards.instructions.md durch.
```

### 2.3 PR-Review Botschaft
```text
Bitte prüfe den PR-Diff auf DAX-, TMDL- und PBIR-Regeln aus .github/copilot-instructions.md
und nenne nur konkrete Verstöße mit kurzer Korrekturempfehlung.
```

## 3) Live-Checkpunkte
- „Umsatz Übersicht (alt)“ muss als absichtlich fehlerhafte Seite vorhanden sein.
- `/review-report` muss mindestens 3 Verstöße finden:
  1. Kreisdiagramm
  2. Titel ohne Einheit/Zeitraum
  3. implizite Aggregation statt explizitem Measure
- CI-Dateien für GitHub und Azure DevOps vorhanden.

## 4) Wenn etwas ausfällt
1. MCP instabil → VS Code neu laden, dann Backup-Branch zeigen.
2. Copilot langsam → vorbereitete Prompts aus diesem Runbook erneut einfügen.
3. Pipeline/Cloud nicht verfügbar → lokal nur Diff + Regeln + vorbereitete Screenshots zeigen.
