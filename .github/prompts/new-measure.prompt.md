---
description: 'Neues KPI-Measure nach Standard anlegen – mit Testeintrag'
---
Lege das Measure ${input:name} an. Fachliche Definition: ${input:definition}.
1. Ist der Power-BI-MCP-Server verbunden, lege es im verbundenen Modell an, sonst in der TMDL-Datei der passenden Tabelle.
   Mit Beschreibung, formatString und displayFolder unter KPI\<Bereich>. Baue auf den Basis-Measures auf.
2. Prüfe es mit einer DAX-Abfrage auf zwei Ebenen (z. B. Store[Country] und 'Date'[Year]) und zeige das Ergebnis.
3. Ergänze den Eintrag in tests/catalog.yml: Typ und Ebenen nach .github/instructions/dax-tests.instructions.md.
4. Erinnere mich, in Power BI Desktop zu speichern (Strg+S). Danach die Tasks „BPA: check model“ und „Tests: check catalog“.
5. Gib mir drei Zeilen für die Pull-Request-Beschreibung.
