# TASK-083 — explain-error-propagation

**Catégorie** : explanation
**Difficulté** : hard
**Artefact(s) lié(s)** : —
**Type de scoring** : `llm_judge`

## Prompt (envoyé à l'agent)

> Dans ce projet, comment les erreurs sont-elles propagées depuis la DB (ex: `NotFoundError`, `ValidationError`) jusqu'au client HTTP ? Réponds :
> 1. Où sont définies les exceptions custom ?
> 2. Y a-t-il un exception handler global (FastAPI `@app.exception_handler` ou équivalent) ?
> 3. Quel mapping exception → HTTP status ?
> 4. Les erreurs sont-elles loguées avant d'être catched ? Où ?

## Réponse attendue

```json
{
  "rubric": {
    "score_2_criteria": [
      "Cite le fichier des exceptions custom avec nom de classe",
      "Indique si un exception_handler global existe (avec fichier:ligne si oui)",
      "Donne le mapping exception → status même partiel (ex: NotFoundError → 404)",
      "Mentionne le logging (ou son absence)"
    ],
    "score_1_criteria": ["Couvre 2-3 critères"],
    "score_0_criteria": ["Réponse théorique sans lien avec le code du projet"]
  }
}
```

## Scoring

- **2** : 4/4 critères
- **1** : 2-3/4
- **0** : 0-1/4

## Notes pour le juge

Multi-fichier : `apps/api/utils/errors.py`, `apps/api/main.py` (pour le handler global). La qualité de la réponse dépend de la complétude du tracing.
