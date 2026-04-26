# TASK-079 — write-tests-parametrize

**Catégorie** : writing_tests
**Difficulté** : medium
**Artefact(s) lié(s)** : —
**Type de scoring** : `contains_all`

## Prompt (envoyé à l'agent)

> Prends la fonction `is_valid_email(email: str) -> bool`. Écris un test paramétrisé avec `pytest.mark.parametrize` qui couvre **au moins 12 cas** : 6 valides, 6 invalides. Chaque paramétrisation doit avoir un `id=` lisible (via `pytest.param(..., id="xxx")` ou `ids=[...]`). Place dans `tests/test_email_validation.py`.

## Réponse attendue

```json
{
  "expected_tokens": [
    "pytest.mark.parametrize",
    "import pytest",
    "is_valid_email",
    "pytest.param",
    "ids=",
    "def test_",
    "assert",
    "True",
    "False",
    "tests/test_email_validation.py"
  ]
}
```

## Scoring

- **2** : ≥ 8/10 tokens (parametrize complet + ids + ≥ 12 cas visibles)
- **1** : 5-7/10
- **0** : < 5/10

## Notes pour le juge

Scroll la longueur de la liste parametrize : si < 12 entrées, -1 point même si tous les tokens présents.
