# TASK-065 — bug-fix-memory-leak

**Catégorie** : bug_fixing
**Difficulté** : hard
**Artefact(s) lié(s)** : —
**Type de scoring** : `contains_all`

## Prompt (envoyé à l'agent)

> Ce handler WebSocket fuit de la mémoire sur un déploiement long :
>
> ```python
> _connections = {}
> async def handle_ws(ws, client_id):
>     _connections[client_id] = ws
>     async for msg in ws:
>         await process(msg)
> ```
>
> Quelle est la fuite ? Donne le fix. Explique ce qui se passe côté `_connections` dans les 3 cas : client ferme proprement, crash réseau, `process()` lève une exception.

## Réponse attendue

```json
{
  "expected_tokens": [
    "try",
    "finally",
    "_connections.pop",
    "cleanup",
    "del _connections",
    "exception",
    "disconnect"
  ]
}
```

## Scoring

- **2** : ≥ 6/7 tokens (try/finally + pop en cleanup + couvre les 3 cas)
- **1** : 3-5/7
- **0** : < 3/7

## Notes pour le juge

Point clé : `try/finally` autour du `async for`. Sans finally, sur exception, l'entrée reste pour toujours et on fuit aussi le ws object. `pop(client_id, None)` pour idempotence.
