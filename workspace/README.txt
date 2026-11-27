Hier den Power-BI-Projektordner ablegen (Datei → Speichern unter → Power-BI-Projekt, TMDL-Format),
z. B. Contoso.SemanticModel und Contoso.Report.

ContosoDemo10k.pbix.Report enthaelt zusaetzlich zwei Analyseseiten:
- Umsatz & Absatz: monatlicher Umsatz und Absatz sowie eindeutige Kunden je Filialland.
- Sortiment & Marge: Umsatz und absolute Marge je Kategorie sowie Absatz und eindeutige Kunden.
Beide Seiten verwenden vorhandene explizite Measures und Filter fuer Bestelljahr,
Filialland und Produktkategorie. WE bezeichnet die Waehrungseinheiten der Demodaten,
nicht EUR. Ohne Filter gilt der gesamte Datenzeitraum. Eindeutige Kunden sind
ueber Laender und Kategorien nicht additiv. Das bestehende Measure "Marge %"
wird wegen seiner Mittelung von Filialquoten auf diesen Seiten nicht verwendet.
Bestehende Seiten, Modellverknuepfung und Theme bleiben unveraendert.
