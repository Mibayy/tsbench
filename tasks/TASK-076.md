# TASK-076 — write-tests-async-fn

**Catégorie** : writing_tests
**Difficulté** : medium
**Artefact(s) lié(s)** : —
**Type de scoring** : `contains_all`

## Prompt (envoyé à l'agent)

> Écris des tests pytest pour une fonction asynchrone `async def fetch_user(user_id: int) -> dict | None` qui fait un HTTP GET via `httpx.AsyncClient`. Mock le client avec `respx` ou `pytest-httpx`. Couvre : succès 200, 404 → None, 500 → raises, timeout → raises `httpx.TimeoutException`. Place dans `tests/test_fetch_user.py`. Utilise `pytest-asyncio` (`@pytest.mark.asyncio`).

## Réponse attendue

```json
{
  "expected_tokens": [
    "import pytest",
    "@pytest.mark.asyncio",
    "async def test_",
    "httpx",
    "respx",
    "200",
    "404",
    "pytest.raises",
    "timeout"
  ]
}
```

## Scoring

- **2** : ≥ 7/9 tokens (async marker + 4 cas + mock)
- **1** : 4-6/9
- **0** : < 4/9

## Notes pour le juge

Alternative acceptée : `unittest.mock.AsyncMock` sur l'`AsyncClient` si respx pas dispo. L'important : `@pytest.mark.asyncio` + couverture des 4 codes.
