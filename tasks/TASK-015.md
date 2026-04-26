# TASK-015 -- insert-near-symbol

**Categorie** : edit
**Difficulte** : medium
**Artefact(s) lie(s)** :
**Type de scoring** : `edit_quality`

## Prompt (envoye a l'agent)

> Insere une nouvelle fonction `validate_invoice_total(invoice: dict) -> bool` juste apres la fonction `calculate_invoice` dans `apps/api/services/billing.py`. La fonction doit verifier que invoice["total"] > 0 et retourner True/False.

## Réponse attendue

```json
{
  "must_contain": [
    "validate_invoice_total",
    "calculate_invoice",
    "total"
  ]
}
```

## Scoring

- **2** : fonction inseree au bon endroit (apres calculate_invoice, ligne ~47) avec le bon contenu
- **1** : fonction inseree mais position ou contenu incorrect
- **0** : pas d'insertion

## Notes pour le juge

Teste `insert_near_symbol` avec disallowed Edit/Write. calculate_invoice est aux lignes 14-46.
