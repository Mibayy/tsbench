# TASK-032 — test-selection-unit

**Catégorie** : testing
**Difficulté** : easy
**Artefact(s) lié(s)** : —
**Type de scoring** : `set_match_strict`

## Prompt (envoyé à l'agent)

> Quels fichiers de test couvrent le module `apps/api/services/billing` ?

## Réponse attendue

```json
{
  "expected_test_files": [
    "tests/test_billing.py"
  ],
  "source_module": "apps/api/services/billing.py"
}
```

## Scoring

- **2** : liste exactement égale à la liste attendue (F1 = 1.0)
- **1** : F1 ≥ 0.75 (un ou deux éléments manquants ou en trop)
- **0** : F1 < 0.75

## Notes pour le juge

Un seul test file correspond.
