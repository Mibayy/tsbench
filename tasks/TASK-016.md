# TASK-016 — test-impact

**Catégorie** : impact
**Difficulté** : medium
**Artefact(s) lié(s)** : BREAK-001
**Type de scoring** : `set_match_loose`

## Prompt (envoyé à l'agent)

> Je viens de modifier la fonction `calculate_invoice` dans `apps/api/services/billing.py`. Quels fichiers de test devrais-je rejouer en priorité ?

## Réponse attendue

```json
{
  "source_symbol": "calculate_invoice",
  "source_file": "apps/api/services/billing.py",
  "expected_test_files": [
    "tests/test_billing.py"
  ]
}
```

## Scoring

- **2** : la réponse contient au moins N éléments corrects parmi ceux attendus
- **1** : au moins la moitié des éléments attendus sont cités
- **0** : aucun élément correct

## Notes pour le juge

Un seul test file couvre billing dans la suite générée.
