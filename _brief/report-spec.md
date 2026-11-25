# Report-Spezifikation: Filialverkauf

## Reportidentität
- Report: ContosoDemo10k – Ergänzung für Filialleitungen
- Semantisches Modell: `ContosoDemo10k.pbix.SemanticModel`
- Zielgruppe: Filialleitungen
- Zweck: Filialumsatz und Marge zeitlich verfolgen und anschließend Produkt- und Unterkategorien als Umsatztreiber untersuchen.
- Ziel: Zwei neue Seiten an den bestehenden lokalen Report anhängen. Die beiden aktiven Bestandsseiten und alle vorhandenen, nicht gespeicherten Änderungen bleiben unangetastet. Der Report hat danach vier aktive Seiten.
- Bestand: `pages.json` registriert zwei aktive Seiten; ein weiterer Seitenordner ist nicht in der aktiven Reihenfolge enthalten und bleibt unberührt.
- Bereitstellung: Lokal im bestehenden PBIR-Projekt; kein Fabric-Publishing.

## Modellbindung
- Einstiegsmodus: Local Model
- Modellname: `ContosoDemo10k`
- Projektpfad: `workspace/ContosoDemo10k.pbix.SemanticModel`
- Binding: `byPath ../ContosoDemo10k.pbix.SemanticModel`
- Reportprojekt: `workspace/ContosoDemo10k.pbix.Report`

## Umfang und Entscheidungen
- Seitenanzahl: Zwei neue Seiten; bestehende aktive Seiten nicht ändern oder entfernen.
- Berichtsnavigation: vorhandene Power-BI-Seitennavigation/Page Navigator; keine Änderungen an Bestandsseiten.
- Gemeinsame Filter der beiden neuen Seiten: `Store[Name]` (Dropdown mit Suche, Einzelauswahl) und `'Date'[Year]` (Dropdown); zwischen den neuen Seiten synchronisieren.
- Zusätzlicher Filter: keiner. Produktkategorien werden auf der zweiten Seite direkt verglichen, nicht durch einen Filter ausgeblendet.
- Interaktionen: Standardmäßiges Cross-Filtering innerhalb jeder neuen Seite; die Store- und Jahresauswahl bleibt zwischen den beiden neuen Seiten synchron.
- Sicherheit: Der Store-Filter ist keine Zugriffsbeschränkung. RLS wird nicht geändert.
- Gestaltung: Bestehendes 1920×1080-Format sowie das registrierte Theme „SQLBI Demo“ beibehalten; keine Neugestaltung der vorhandenen Seiten. Neue Seiten übernehmen dessen neutrale Oberfläche und Tabellenbandierung. Nur notwendige Visual-Overrides, insbesondere für gut lesbare Achsenbeschriftungen, sind vorgesehen.
- Barrierefreiheit: Aussagekräftiger Alt-Text für jedes Visual, logische Tab-Reihenfolge, ausreichender Kontrast, Farbe nie als einziges Unterscheidungsmerkmal.

## KPIs
1. **Umsatz** — bestehendes Measure `Sales[Umsatz]`; Karten- und Tabellenformat erst nach Klärung der Währung festlegen.
2. **Marge** — bestehendes Measure `Sales[Marge]`; als monetärer Wert in derselben Währung wie der Umsatz.
3. **Marge %** — bestehendes Measure `Sales[Marge %]`, muss vor Verwendung korrigiert werden auf `DIVIDE ( [Marge], [Umsatz] )`; keine Mittelung einzelner Filialquoten.
4. **Absatz Stück** — bestehendes Measure `Sales[Absatz Stück]`; ganzzahlig, als Stückzahl formatiert.

Alle vier KPIs sind explizite Measures. Die bestehenden Einträge in `tests/catalog.yml` decken diese Measures bereits ab; insbesondere bleibt der Quotiententest für `Marge %` bestehen und muss nach der Korrektur ausgeführt werden. Beschreibungen, passende `formatString`-Werte und KPI-Ordner sind für die sichtbaren KPIs sowie die Measure-Abhängigkeit `Kosten` zu ergänzen bzw. zu prüfen.

## Seitenplan
1. **Umsatz im gewählten Jahr** — Analytical Canvas, Inline-Slicer-Variante. Zweck: die ausgewählte Filiale über den Zeitverlauf einschätzen. Vier kompakte KPI-Karten, Monatsverläufe für Umsatz und Marge sowie eine kompakte Kennzahlentabelle nach Produktkategorie. Monatsachse: `'Date'[Year Month Short]`, nach `'Date'[Year Month Number]` sortiert.
2. **Produktleistung im gewählten Jahr** — Analytical Canvas, Small-Multiples-Variante. Zweck: Umsatzverlauf je Produktkategorie vergleichen und anschließend Unterkategorien sowie Produkte identifizieren. Visuals: Umsatzverläufe je `Product[Category]` mit gemeinsamer Y-Achse, nach Umsatz sortierte Top-12-Unterkategorien und Top-15-Produkte mit Umsatz, Marge, Marge % und Stückzahl.

## Modell- und Datenanforderungen
- Faktengranularität: `Sales` enthält Verkaufspositionen; weder eine Bestellanzahl noch ein durchschnittlicher Warenkorb wird behauptet.
- Modellbeziehungen und vorhandene Beziehungen bleiben unverändert.
- **Währungsprüfung vor dem Bau erforderlich:** `Sales[Currency Code]` und `Sales[Exchange Rate]` sind vorhanden, aber die aktuellen Umsatz-/Kosten-Measures rechnen den Wechselkurs nicht ein. Vor Verwendung als vergleichbare monetäre Summen ist zu prüfen, ob jede ausgewählte Filiale genau eine Währung führt und wie der Wechselkurs definiert ist. Ohne diese Prüfung keine Euro-Kennzeichnung und keine Summierung über mehrere Währungen. Falls Umrechnung nötig ist, ist die Berechnung je Zeile vor Aggregation festzulegen; die Richtung des Wechselkurses wird nicht angenommen.
- Das Modell enthält keine Bestands-, Retouren-, Budget-/Ziel-, Frequenz- oder Personalkennzahlen. Aussagen zu Verfügbarkeit, Planerreichung, Retourenquote, Conversion oder Produktivität sind daher nicht Teil des Reports.
- `Store[Name]` dient zur Auswahl, nicht zur Absicherung des Datenzugriffs. Eine gewünschte Filialbeschränkung per RLS wäre separat anzufragen.

## Umsetzungs- und Prüfgrenze
- Vor PBIR-Änderungen die freigegebene Spezifikation erneut prüfen.
- Die lokale Report- und Modelldateien enthalten bereits nicht gespeicherte Änderungen; diese bleiben erhalten und werden nicht überschrieben.
- Vor Visualisierung der KPIs Währungsprüfung und Korrektur von `Marge %` durchführen. Keine Änderung an Beziehungen, Datenquellen, Partitionen oder Rollen.
- Für geänderte Measures die vorhandenen Katalogtests prüfen und anschließend die Tasks „BPA: check model“ und „Tests: check catalog“ ausführen; Stufe-3-Funde beheben.
- Power BI Desktop-Preview-Verfügbarkeit ist noch nicht geprüft. Nach Änderungen in Power BI Desktop speichern (Strg+S), bevor BPA, Diff oder Tests als maßgeblich gelten.
- Veröffentlichung ist nicht angefragt und bleibt außerhalb dieses Umfangs.

## Kanonischer Designvertrag

```yaml
Design Brief:
  generated_by: powerbi-report-cli
  contract_version: 1
  mode: brownfield
  design_identity:
    tone: "SQLBI Demo neutral: weiße Flächen, dunkle Beschriftungen und dezente graue Tabellenbandierung; vorhandenes Theme bleibt bestehen."
    signature: "Die neuen Seiten verwenden dunkle Ist-Werte, konsistente Zahlenformate und dieselbe zurückhaltende Tabellenbandierung."
    current_tone: "SQLBI Demo Theme: weiße Oberfläche, charcoal Text, graue Tabellenbandierung und umfangreiche Datenfarben."
    current_signature: "Keine eindeutige reportweite Signatur allein aus dem Theme ableitbar."
  brownfield_delta: "Zwei neue Seiten ergänzen den bestehenden Report; Canvas, Theme, aktive Bestandsseiten und vorhandene lokale Änderungen bleiben erhalten."
  archetype: Analytical Canvas
  navigation_model: page_navigator
  color_map:
    - measure: Sales[Umsatz]
      color: "#131312"
      tint: "#E5E0DA"
    - measure: Sales[Marge]
      color: "#3F3F3F"
      tint: "#ECECEC"
    - measure: Sales[Marge %]
      color: "#6C6966"
      tint: "#E5E0DA"
    - measure: Sales[Absatz Stück]
      color: "#5F5E5C"
      tint: "#ECECEC"
  pages:
    - name: Umsatz im gewählten Jahr
      role: detail
      archetype: Analytical
      layout_variant: B
      variant_rationale: "Zwei gemeinsame Filter passen zur Inline-Slicer-Variante und lassen die gesamte Inhaltsbreite für den Filialüberblick frei."
      navigation: []
      page_background: "#FFFFFF"
      layout_summary: "Kompakte KPI-Zeile über zwei Zeitreihen und einer Kategorieübersicht; keine Werte werden ohne bestätigte Währung als Euro bezeichnet."
      layout_contract:
        canvas:
          width: 1920
          height: 1080
          margin: 32
          gutter: 24
          snap: 8
        grid:
          columns: 12
          rows: 12
          regions:
            header: [1, 1, 9, 2]
            filters: [9, 1, 13, 2]
            kpis: [1, 2, 13, 4]
            revenue_trend: [1, 4, 8, 9]
            margin_trend: [8, 4, 13, 9]
            category_detail: [1, 9, 13, 13]
        placements:
          - id: page_title
            region: header
            kind: textbox
            text: "Umsatz (Modellwährung) | Monatsverlauf im gewählten Jahr"
            purpose: "Nennt Kennzahl, Währungskontext und Zeitraum der Seite."
          - id: store_slicer
            region: filters
            kind: slicer
            field_bindings: Store[Name]
            slicer_type: dropdown
            slot: 1
            of: 2
          - id: year_slicer
            region: filters
            kind: slicer
            field_bindings: "'Date'[Year]"
            slicer_type: dropdown
            slot: 2
            of: 2
          - id: revenue_kpi
            region: kpis
            kind: cardVisual
            purpose: "Wie hoch ist der Umsatz der ausgewählten Filiale im ausgewählten Jahr?"
            subtitle: "Filiale und Jahr gemäß aktiver Auswahl"
            field_bindings: Sales[Umsatz]
            color_strategy: measure_match
            slot: 1
            of: 4
          - id: margin_kpi
            region: kpis
            kind: cardVisual
            purpose: "Wie hoch ist die Marge der ausgewählten Filiale im ausgewählten Jahr?"
            subtitle: "Filiale und Jahr gemäß aktiver Auswahl"
            field_bindings: Sales[Marge]
            color_strategy: measure_match
            slot: 2
            of: 4
          - id: margin_pct_kpi
            region: kpis
            kind: cardVisual
            purpose: "Welchen Anteil am Umsatz hat die Marge der ausgewählten Filiale?"
            subtitle: "Filiale und Jahr gemäß aktiver Auswahl"
            field_bindings: Sales[Marge %]
            color_strategy: measure_match
            slot: 3
            of: 4
          - id: units_kpi
            region: kpis
            kind: cardVisual
            purpose: "Wie viele Stück wurden in der ausgewählten Filiale verkauft?"
            subtitle: "Filiale und Jahr gemäß aktiver Auswahl"
            field_bindings: Sales[Absatz Stück]
            color_strategy: measure_match
            slot: 4
            of: 4
          - id: monthly_revenue
            region: revenue_trend
            kind: lineChart
            purpose: "Wie entwickelt sich der Umsatz Monat für Monat?"
            field_bindings:
              Category: "'Date'[Year Month Short]"
              Y: Sales[Umsatz]
            sort_policy: natural_order
            color_strategy: measure_match
          - id: monthly_margin
            region: margin_trend
            kind: lineChart
            purpose: "Wie entwickelt sich die Marge Monat für Monat?"
            field_bindings:
              Category: "'Date'[Year Month Short]"
              Y: Sales[Marge]
            sort_policy: natural_order
            color_strategy: measure_match
          - id: category_detail
            region: category_detail
            kind: tableEx
            purpose: "Welche Produktkategorien tragen Umsatz, Marge und Absatz?"
            field_bindings:
              - Product[Category]
              - Sales[Umsatz]
              - Sales[Marge]
              - Sales[Marge %]
              - Sales[Absatz Stück]
            sort_policy: value_desc
            sort_by: Sales[Umsatz]
            color_strategy: measure_match
        space_audit:
          content_cell_count: 132
          placed_cell_count: 132
          empty_cell_pct: 0
          unplaced_regions: []
          largest_region:
            name: category_detail
            pct_of_content: 36.4
          balance_rationale: "Vier kompakte KPI-Karten belegen zwei Zeilen; zwei getrennte Zeitreihen vermeiden eine duale Achse; die Kategorie-Tabelle nutzt vier Zeilen für genaue Werte."
    - name: Produktleistung im gewählten Jahr
      role: detail
      archetype: Analytical
      layout_variant: C
      variant_rationale: "Der Schwerpunkt ist der Vergleich der Produktkategorien über denselben Monatsverlauf; Small Multiples mit gemeinsamer Werteachse machen die Kategorien direkt vergleichbar."
      navigation: []
      page_background: "#FFFFFF"
      layout_summary: "Gemeinsame Filial- und Jahresfilter, Kategorieverläufe auf gemeinsamer Skala, danach eine sortierte Unterkategorienrangliste und eine begrenzte Produkttabelle."
      layout_contract:
        canvas:
          width: 1920
          height: 1080
          margin: 32
          gutter: 24
          snap: 8
        grid:
          columns: 12
          rows: 12
          regions:
            header: [1, 1, 9, 2]
            filters: [9, 1, 13, 2]
            category_trends: [1, 2, 13, 7]
            subcategory_ranking: [1, 7, 7, 13]
            product_detail: [7, 7, 13, 13]
        placements:
          - id: page_title
            region: header
            kind: textbox
            text: "Umsatz (Modellwährung) & Marge (%) | Produktleistung im gewählten Jahr"
            purpose: "Nennt Kennzahlen, Währungskontext und Zeitraum der Produktanalyse."
          - id: store_slicer
            region: filters
            kind: slicer
            field_bindings: Store[Name]
            slicer_type: dropdown
            slot: 1
            of: 2
          - id: year_slicer
            region: filters
            kind: slicer
            field_bindings: "'Date'[Year]"
            slicer_type: dropdown
            slot: 2
            of: 2
          - id: category_monthly_trends
            region: category_trends
            kind: smallMultiplesChart
            purpose: "Wie unterscheidet sich der monatliche Umsatzverlauf zwischen Produktkategorien?"
            field_bindings:
              Category: "'Date'[Year Month Short]"
              Y: Sales[Umsatz]
              Small multiples: Product[Category]
            sort_policy: natural_order
            color_strategy: measure_match
            shared_y_axis: true
          - id: subcategory_ranking
            region: subcategory_ranking
            kind: barChart
            purpose: "Welche Unterkategorien erzielen den höchsten Umsatz?"
            field_bindings:
              Category: Product[Subcategory]
              Y: Sales[Umsatz]
            sort_policy: value_desc
            sort_by: Sales[Umsatz]
            top_n: 12
            color_strategy: measure_match
          - id: top_products
            region: product_detail
            kind: tableEx
            purpose: "Welche einzelnen Produkte führen bei Umsatz, Marge und Stückzahl?"
            field_bindings:
              - Product[Product Name]
              - Product[Subcategory]
              - Sales[Umsatz]
              - Sales[Marge]
              - Sales[Marge %]
              - Sales[Absatz Stück]
            sort_policy: value_desc
            sort_by: Sales[Umsatz]
            top_n: 15
            color_strategy: measure_match
        space_audit:
          content_cell_count: 132
          placed_cell_count: 132
          empty_cell_pct: 0
          unplaced_regions: []
          largest_region:
            name: category_trends
            pct_of_content: 45.5
          balance_rationale: "Die Kategorieverläufe bekommen die größte Fläche; Unterkategorienranking und Top-15-Tabelle teilen die untere Hälfte und bleiben jeweils sechs Rasterzeilen hoch."
  interaction_pattern:
    drill_targets: []
    cross_filter_rules: "Standardmäßiges Cross-Filtering innerhalb der Visuals jeder neuen Seite; Store- und Jahresfilter zwischen den beiden neuen Seiten synchronisieren."
  accessibility:
    alt_text_strategy: "Jedes Visual erhält einen Alt-Text mit Kennzahl, Dimension, Zeitraum und Filterkontext; keine Ergebnisse werden vor einer Datenprüfung behauptet."
    contrast_notes: "Bestehende neutrale Theme-Farben erhalten; Text mindestens WCAG AA, Diagrammfarben mindestens 3:1. Unterschiede zusätzlich durch Beschriftung vermitteln, nicht allein über Farbe."
  theme:
    base: "Vorhandenes SQLBI Demo Theme und Fluent2-CY26SU08 Basistheme beibehalten."
    user_overrides: "Keine Theme-Neuregistrierung und keine Änderung bestehender Seiten; neue Visuals erhalten nur notwendige lesbare Achsen-, Einheiten-, Titel- und Alt-Text-Overrides."
```
