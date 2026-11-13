---
name: 'TMDL model files'
description: 'Use when creating or changing tables, measures or relationships in TMDL.'
applyTo: '**/*.tmdl'
---
- If the model is open in Power BI Desktop and connected through the Power BI MCP server, change it through MCP – not in these files.
  Desktop overwrites the files on save.
- Descriptions go in /// lines directly above the object.
- Keep tab indentation exactly as TMDL requires.
- Do not reorder existing objects (keeps the Git diff small and reviewable).
- Do not touch lineageTag values.
