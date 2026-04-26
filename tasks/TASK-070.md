# TASK-070 — refactor-sync-to-async

**Catégorie** : refactoring
**Difficulté** : hard
**Artefact(s) lié(s)** : —
**Type de scoring** : `contains_all`

## Prompt (envoyé à l'agent)

> Cette fonction synchrone fait 3 HTTP calls séquentiels, lent :
>
> ```python
> def fetch_all(user_id: int):
>     profile = requests.get(f"{API}/users/{user_id}").json()
>     orders = requests.get(f"{API}/orders?user={user_id}").json()
>     settings = requests.get(f"{API}/settings/{user_id}").json()
>     return {"profile": profile, "orders": orders, "settings": settings}
> ```
>
> Refactor en `async def fetch_all(user_id: int)` avec `httpx.AsyncClient` et les 3 calls en parallèle via `asyncio.gather`. Gère aussi une exception sur l'un des 3 sans tout faire crasher (retourne `None` pour le champ qui a foiré).

## Réponse attendue

```json
{
  "expected_tokens": [
    "async def fetch_all",
    "httpx.AsyncClient",
    "asyncio.gather",
    "return_exceptions=True",
    "await",
    "isinstance",
    "Exception"
  ]
}
```

## Scoring

- **2** : ≥ 6/7 tokens (async + parallel gather + exception handling)
- **1** : 3-5/7
- **0** : < 3/7

## Notes pour le juge

`return_exceptions=True` sur `gather` puis filtrer les exceptions pour mettre `None`. Alternative acceptée : 3 try/except individuels en `await asyncio.to_thread(...)`.
