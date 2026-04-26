# TASK-023 — explain-billing-module

**Catégorie** : heavy_read
**Difficulté** : hard
**Artefact(s) lié(s)** :
**Type de scoring** : `contains_all`

## Prompt (envoyé à l'agent)

> Explique l'implémentation complète du module `apps/api/services/billing.py`. Liste les fonctions publiques principales (calculate_invoice, apply_discount, charge_customer, refund_payment, list_invoices, void_invoice) avec une phrase sur le rôle de chacune.

## Réponse attendue

```json
{
  "must_contain": [
    "calculate_invoice",
    "apply_discount",
    "charge_customer",
    "refund_payment",
    "list_invoices",
    "void_invoice"
  ]
}
```

## Scoring

- **2** : toutes les 6 fonctions publiques mentionnées
- **1** : ≥3 fonctions mentionnées
- **0** : <3

## Notes pour le juge

Fichier de 648 lignes. Le baseline doit lire le fichier entier via Read ; TS peut utiliser `get_functions` ou `get_file_structure` pour obtenir juste les signatures.
