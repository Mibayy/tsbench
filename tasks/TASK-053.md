# TASK-053 — code-gen-middleware-logger

**Catégorie** : code_generation
**Difficulté** : medium
**Artefact(s) lié(s)** : —
**Type de scoring** : `contains_all`

## Prompt (envoyé à l'agent)

> Implémente une middleware FastAPI `LoggingMiddleware` dans `apps/api/middleware/logging_mw.py` (nouveau fichier). Elle log méthode, path, status, duration_ms pour chaque requête. Utilise `starlette.middleware.base.BaseHTTPMiddleware`. Capture le status même en cas d'exception (log `status=500` puis re-raise).

## Réponse attendue

```json
{
  "expected_tokens": [
    "class LoggingMiddleware",
    "BaseHTTPMiddleware",
    "async def dispatch",
    "time.perf_counter",
    "duration_ms",
    "try",
    "except",
    "raise",
    "apps/api/middleware/logging_mw.py"
  ]
}
```

## Scoring

- **2** : ≥ 7/9 tokens
- **1** : 4-6/9
- **0** : < 4/9

## Notes pour le juge

`BaseHTTPMiddleware.dispatch` reçoit `(request, call_next)`. Le try/except autour de `call_next` permet de logger les 500. Oublier de re-raise après log = bug.
