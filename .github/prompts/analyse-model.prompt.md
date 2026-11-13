---
description: 'Verbesserungspotenzial des verbundenen Modells ermitteln – ohne Änderungen'
---
Analysiere das über den Power-BI-MCP-Server verbundene Modell gegen .github/copilot-instructions.md.
Nutze dazu auch die BPA-Ergebnisse in bpa-*.txt (falls vorhanden).
Prüfe insbesondere:
- Measures, die über Ebenen falsch rechnen können (z. B. gemittelte Prozente, "/" statt DIVIDE)
- Beziehungen: Richtung, inaktive Beziehungen und wie sie genutzt werden
- sichtbare numerische Spalten (Risiko Auto-Summierung)
- fehlende Beschreibungen, Formate und Ordner
- was Copilot und Agents für korrekte Antworten noch fehlt
Liefere eine Tabelle: Priorität | Fund | Auswirkung auf Zahlen oder KI | Aufwand | Vorschlag.
Ändere nichts.
