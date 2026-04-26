# TASK-078 — write-tests-integration

**Catégorie** : writing_tests
**Difficulté** : hard
**Artefact(s) lié(s)** : —
**Type de scoring** : `contains_all`

## Prompt (envoyé à l'agent)

> Écris un test d'intégration pytest pour le endpoint `POST /api/orders` (FastAPI). Utilise `TestClient`. Scénario bout-en-bout :
> 1. Crée un user via fixture `db_session`
> 2. Authentifie-le (Bearer token dans header)
> 3. POST payload valide → 201, retourne `order.id`
> 4. Vérifie en DB que l'order existe avec le bon user_id
> 5. Vérifie qu'un email de confirmation a été "envoyé" (mock `send_email`)
>
> Place dans `tests/integration/test_orders_api.py`.

## Réponse attendue

```json
{
  "expected_tokens": [
    "TestClient",
    "from fastapi.testclient",
    "@pytest.fixture",
    "db_session",
    "Bearer",
    "Authorization",
    "mocker.patch",
    "send_email",
    "tests/integration/test_orders_api.py"
  ]
}
```

## Scoring

- **2** : ≥ 7/9 tokens (fixture + auth + mock + assertion DB)
- **1** : 4-6/9
- **0** : < 4/9

## Notes pour le juge

Intégration = plusieurs couches ensemble. Si le test ne mock rien et n'a pas de fixture DB, ce n'est pas un vrai test d'intégration.
