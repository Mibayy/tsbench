# TASK-077 — write-tests-error-paths

**Catégorie** : writing_tests
**Difficulté** : medium
**Artefact(s) lié(s)** : —
**Type de scoring** : `contains_all`

## Prompt (envoyé à l'agent)

> Pour la fonction `apply_discount(payload: dict, user_id: int = 0)` dans `apps/api/services/billing.py`, écris exclusivement des **tests d'error paths** dans `tests/test_apply_discount_errors.py`. Au minimum :
> - payload ne contient pas `discount_percent` → ValidationError
> - discount_percent < 0 → ValidationError
> - discount_percent > 100 → ValidationError
> - discount_percent non-numérique → ValidationError ou TypeError
> - user_id négatif → ValidationError (si règle métier)
> - DB down → propagation exception

## Réponse attendue

```json
{
  "expected_tokens": [
    "pytest.raises",
    "ValidationError",
    "discount_percent",
    "def test_",
    "payload",
    "< 0",
    "> 100",
    "tests/test_apply_discount_errors.py"
  ]
}
```

## Scoring

- **2** : ≥ 6/8 tokens (≥ 4 error paths + raises bien utilisé)
- **1** : 3-5/8
- **0** : < 3/8

## Notes pour le juge

Aucun test de happy path dans le fichier. Si l'agent en écrit un = il n'a pas suivi la contrainte. Le fichier doit être monochrome error-path.
