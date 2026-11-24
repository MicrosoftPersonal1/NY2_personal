# New Yorker – Standards für semantische Modelle (Copilot liest diese Datei bei jeder Anfrage)

## Kontext
- Modehandel. Kernmodelle: Umsatz & Marge, Bestand & Warenfluss, Einkauf.
- Modelle liegen als Power-BI-Projekt (TMDL) unter /workspace. Produktion nie direkt ändern.

## Aktuelles Modell (Demo, Contoso-Beispieldaten)
- Faktentabelle: Sales (Bestellpositionen: Quantity, Net Price, Unit Cost …).
- Dimensionen: Customer, Product, Store, 'Date'.
- Beziehungen (n:1, eine Richtung, von Sales zur Dimension):
  - Sales[CustomerKey] → Customer[CustomerKey]
  - Sales[ProductKey] → Product[ProductKey]
  - Sales[StoreKey] → Store[StoreKey]
  - Sales[Order Date] → 'Date'[Date] (aktiv)
  - Sales[Delivery Date] → 'Date'[Date] (inaktiv)
- Ebenen:
  - Store: StoreKey → State → Country
  - Product: ProductKey → Subcategory → Category
  - 'Date': Month → Year
- Spaltennamen immer im verbundenen Modell prüfen, nie raten.

## Arbeiten mit dem Power-BI-MCP-Server
- Ist das Modell über den MCP-Server verbunden: Modelländerungen nur über MCP, nie gleichzeitig die TMDL-Dateien bearbeiten.
  Power BI Desktop überschreibt die Dateien beim Speichern.
- Nach Modelländerungen daran erinnern, in Power BI Desktop zu speichern (Strg+S). Erst danach sehen BPA, Diff und Tests die Änderung.
- Abfragen zum Prüfen sind erlaubt; Änderungen immer einzeln bestätigen lassen.

## Modellstruktur
- Sternschema, Beziehungen 1:n in eine Richtung.
- Eine markierte Datumstabelle, kein Auto-Datum.
- Technische Keys und Faktenspalten ausblenden.

## Measures – damit Copilot und Berichte gleich rechnen
- Jede Kennzahl ist ein explizites Measure – nie Auto-Summierung.
- Namen: deutsche Business-Begriffe ohne Präfix, z. B. Umsatz, Marge %, Umsatz VJ.
- Jedes Measure hat Beschreibung (/// in TMDL bzw. Description), formatString und displayFolder unter KPI\<Bereich>.
- Basis-Measures dieses Modells:
  - Umsatz = SUMX ( Sales, Sales[Quantity] * Sales[Net Price] )
  - Kosten = SUMX ( Sales, Sales[Quantity] * Sales[Unit Cost] )
  - Marge = [Umsatz] - [Kosten]
- Neue Measures bauen auf diesen Basis-Measures auf – keine eigenen SUMs auf Spalten.
- Verhältnisse immer DIVIDE([Zähler], [Nenner]) – nie Prozente mitteln.
- Auswertungen nach Lieferdatum mit CALCULATE ( …, USERELATIONSHIP ( Sales[Delivery Date], 'Date'[Date] ) ).
  Die inaktive Beziehung nie aktivieren.
- Bestand ist semi-additiv: Wert am letzten Tag mit Daten – nie über Tage summieren.
- Eindeutige Anzahlen mit DISTINCTCOUNT, z. B. Kunden über Sales[CustomerKey] – nie über Filialen addieren.
- Währung je Zeile umrechnen, dann aggregieren. Variablen (VAR) statt Wiederholung, kein IFERROR.

## Arbeitsweise (immer)
- Neues oder geändertes KPI-Measure: Eintrag in tests/catalog.yml mitpflegen.
  Regeln dazu: .github/instructions/dax-tests.instructions.md.
- Nach Änderungen die Tasks „BPA: check model“ und „Tests: check catalog“ ausführen und Stufe-3-Funde beheben.
- RLS-Rollen, Datenquellen, Partitionen und Beziehungen nur auf ausdrückliche Anfrage ändern.
- Jede Änderung in einer Zeile erklären – für die PR-Beschreibung.
- Antworten auf Deutsch.

## Beispiel – so (bevorzugt)
```
/// Bruttomarge in % vom Nettoumsatz.
/// Immer Summe Marge ÷ Summe Umsatz.
measure 'Marge %' = DIVIDE ( [Marge], [Umsatz] )
    formatString: 0.0%
    displayFolder: KPI\Marge
```

## Beispiel – nicht so (vermeiden)
```
measure 'Marge %' =
    AVERAGEX ( VALUES ( Store[StoreKey] ), [Marge] / [Umsatz] )
```

## Code Review (Pull Requests)
- Prüfe DAX auf robuste Berechnungen: Verhältnisse mit `DIVIDE`, keine direkte Division mit `/`.
- Prüfe, dass neue Report-Kennzahlen als **explizite Measures** umgesetzt sind.
- Prüfe bei neuen/angepassten Measures: Beschreibung vorhanden, sinnvolles Format, passender KPI-Ordner.
- Prüfe TMDL-Beziehungen: keine bidirektionalen Filter außer dokumentierte Ausnahme mit Begründung im PR.
- Prüfe PBIR-Seiten gegen `.github/instructions/report-standards.instructions.md`.
- Liste in Reviews nur konkrete Verstöße (Datei/Objekt/Regel) plus kurze Korrekturempfehlung.
