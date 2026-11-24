---
description: 'Neue Report-Seite im PBIR-Format erstellen und gegen Report-Standards selbst prüfen.'
---
Erstelle im PBIR-Report eine neue Seite mit:
- Seitenname: ${input:seitenname}
- Fachfrage: ${input:businessfrage}

Vorgehen:
1. Nutze nur bestehende, explizite Measures aus dem Modell (keine impliziten Aggregationen, keine neuen Measures).
2. Setze das Theme `themes/ny-ibcs-demo.json` ein bzw. richte Farben und Formatierung entsprechend aus.
3. Erzeuge eine klare, IBCS-nahe Struktur mit Titel, passenden Visualtypen und nur nötigen Elementen.
4. Prüfe danach die Seite gegen `.github/instructions/report-standards.instructions.md`.
5. Gib als Ergebnis:
   - Kurz, was erstellt wurde.
   - Eine Tabelle mit Abweichungen: `Regel | Befund | Vorschlag`.
   - Falls es keine Abweichung gibt: `Keine Abweichungen gefunden.`
