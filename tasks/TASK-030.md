# TASK-030 -- backward-slice

**Categorie** : navigation
**Difficulte** : hard
**Artefact(s) lie(s)** : HOTSPOT-001
**Type de scoring** : `contains_all`

## Prompt (envoye a l'agent)

> Calcule le backward slice de la fonction `reconcile_payments` dans `apps/api/services/complex_billing.py`. Quels symboles influencent directement ou transitivement cette fonction ?

## Réponse attendue

```json
{
  "must_contain": [
    "reconcile_payments",
    "complex_billing.py"
  ]
}
```

## Scoring

- **2** : backward slice complet avec symboles influencants
- **1** : fonction identifiee + quelques dependances
- **0** : echec

## Notes pour le juge

Teste `get_backward_slice`. Fonction a complexite cyclomatique 14 (HOTSPOT-001). L'analyse de flux de donnees est difficile sans outil structure.
