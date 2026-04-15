# TASK-054 -- fix-buggy-paginate

**Categorie** : edit
**Difficulte** : medium
**Artefact(s) lie(s)** : BUG-001
**Type de scoring** : `edit_quality`

## Prompt (envoye a l'agent)

> La fonction `buggy_paginate` dans `apps/api/utils/buggy_pagination.py` contient un off-by-one : elle retourne 11 items au lieu de 10. Le bug est dans le calcul de `end`. Corrige-la en utilisant replace_symbol_source. Inclus le nom exact de la fonction et du fichier dans ta reponse finale.

## Réponse attendue

```json
{
  "must_contain": [
    "buggy_paginate",
    "buggy_pagination.py",
    "end"
  ]
}
```

## Scoring

- **2** : bug corrige correctement (end = start + page_size, sans le +1)
- **1** : tentative correcte mais code modifie au-dela du necessaire
- **0** : echec ou pas de modification

## Notes pour le juge

Teste `replace_symbol_source` avec disallowed Edit/Write. Le bug reel (BUG-001) : `end = start + page_size + 1` devrait etre `end = start + page_size`.
