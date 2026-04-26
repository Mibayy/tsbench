# TASK-016 — bug-pagination

**Catégorie** : debug
**Difficulté** : medium
**Artefact(s) lié(s)** : BUG-001
**Type de scoring** : `exact_match`

## Prompt (envoyé à l'agent)

> Un utilisateur signale que notre pagination retourne 11 résultats par page au lieu de 10. Où est le bug ?

## Réponse attendue

```json
{
  "file": "apps/api/utils/buggy_pagination.py",
  "symbol": "buggy_paginate",
  "bug_hint": "end = start + page_size + 1"
}
```

## Scoring

- **2** : fichier + symbole + ligne (±3) corrects
- **1** : fichier + symbole corrects, ligne hors tolérance
- **0** : symbole incorrect ou non trouvé

## Notes pour le juge

BUG-001 : off-by-one dans `buggy_paginate`, end index = start + page_size + 1.
