---
description: 'Aggregationstests aus tests/catalog.yml gegen das verbundene Modell ausführen'
---
Führe die Aggregationstests gegen das über den Power-BI-MCP-Server verbundene Modell aus. Umfang: ${input:scope}.
1. Erzeuge die Abfragen im Terminal: `python ci/run_tests.py --print-dax tests/generated.dax --only "<Measure-Namen aus dem Umfang, kommagetrennt>"`
   (bei Umfang „alle“ ohne --only). Lies dann tests/generated.dax.
2. Jede Abfrage beginnt mit einer Kommentarzeile, die die Regel nennt:
   - `[0 rows = PASS]`: PASS, wenn die Abfrage keine Zeilen liefert
   - `[value must not be blank]`: PASS, wenn der Wert nicht leer und nicht 0 ist
   - `[compare with …csv]`: Ergebnis mit der CSV vergleichen, Toleranz 0,01
3. Führe jede Abfrage einzeln über den MCP-Server aus.
4. Zeige eine Tabelle: Test | PASS/FAIL | abweichende Zeilen (höchstens drei Beispiele).
5. Ändere nichts am Modell.
