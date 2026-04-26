# TASK-056 -- checkpoint-restore

**Categorie** : edit
**Difficulte** : hard
**Artefact(s) lie(s)** :
**Type de scoring** : `edit_quality`

## Prompt (envoye a l'agent)

> Workflow complet : 1) Cree un checkpoint du fichier `apps/api/services/billing.py`. 2) Remplace le corps de `charge_customer` pour ajouter un guard `if not payload: raise ValueError("empty payload")` au debut. 3) Compare le checkpoint avec l'etat actuel pour lister les differences.

## Réponse attendue

```json
{
  "must_contain": [
    "checkpoint",
    "charge_customer",
    "billing.py"
  ]
}
```

## Scoring

- **2** : les 3 etapes completees (checkpoint + edit + compare)
- **1** : 2/3 etapes completees
- **0** : <2 etapes

## Notes pour le juge

Teste `create_checkpoint` + `replace_symbol_source` + `compare_checkpoint_by_symbol`. charge_customer est aux lignes 82-114.
