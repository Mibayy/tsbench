# TASK-087 — write-api-reference

**Catégorie** : documentation
**Difficulté** : medium
**Artefact(s) lié(s)** : —
**Type de scoring** : `llm_judge`

## Prompt (envoyé à l'agent)

> Liste et documente les endpoints HTTP du module `apps/api/callers/` (ou équivalent). Pour chaque endpoint : méthode, path, description courte, request body (si applicable), réponse success, erreurs possibles. Format markdown, tableau ou liste. Limite-toi aux 5 endpoints les plus "business" (pas les health checks).

## Réponse attendue

```json
{
  "rubric": {
    "score_2_criteria": [
      "Liste 5 endpoints réels du projet (vérifiables dans apps/api/callers/)",
      "Pour chaque endpoint : méthode + path + description",
      "Request body décrit pour au moins 3 endpoints POST/PUT",
      "Codes d'erreur mentionnés (au moins 401 ou 404 pour 2+ endpoints)"
    ],
    "score_1_criteria": ["3-4 endpoints réels documentés partiellement"],
    "score_0_criteria": ["Endpoints inventés ou juste 1-2 endpoints trouvés"]
  }
}
```

## Scoring

- **2** : 4/4 critères
- **1** : 2-3/4
- **0** : 0-1/4

## Notes pour le juge

Test de navigation + doc. TS devrait utiliser `get_routes` (si supporté) ou `list_files apps/api/callers/`. Natif : Read + Grep `@app.post` / `@router.get`.
