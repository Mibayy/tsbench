# TASK-038 — module-overview

**Catégorie** : onboarding
**Difficulté** : medium
**Artefact(s) lié(s)** : —
**Type de scoring** : `free_form_rubric`

## Prompt (envoyé à l'agent)

> Explique l'architecture du module `apps/api/services/billing.py` : quelles sont ses responsabilités, ses fonctions principales, et ses dépendances ?

## Réponse attendue

```json
{
  "module": "apps/api/services/billing.py",
  "key_functions": [
    "calculate_invoice",
    "apply_discount",
    "charge_customer",
    "refund_payment"
  ],
  "dependencies": [
    "apps/api/db",
    "apps/api/models/billing",
    "apps/api/config",
    "apps/api/utils/logging"
  ]
}
```

## Scoring

- **2** : couvre tous les points clés demandés, sans invention
- **1** : couvre la majorité des points mais en oublie ou invente un détail secondaire
- **0** : réponse incorrecte, très incomplète, ou hallucinations majeures

## Notes pour le juge

Réponse correcte mentionne les fonctions principales et les imports (calculate_invoice a été renommé depuis compute_invoice via BREAK-001).
