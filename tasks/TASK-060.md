# TASK-060 — bug-fix-off-by-one

**Catégorie** : bug_fixing
**Difficulté** : easy
**Artefact(s) lié(s)** : —
**Type de scoring** : `contains_all`

## Prompt (envoyé à l'agent)

> Dans `packages/utils/paginate.py` (fichier fictif pour ce prompt), une fonction `paginate(items, page, per_page)` a ce bug :
>
> ```python
> start = (page - 1) * per_page
> end = start + per_page - 1   # BUG ici
> return items[start:end]
> ```
>
> Identifie le bug et donne le fix exact. Indique le fichier et la ligne.

## Réponse attendue

```json
{
  "expected_tokens": [
    "off-by-one",
    "end = start + per_page",
    "start + per_page",
    "paginate",
    "per_page",
    "items[start:end]"
  ]
}
```

## Scoring

- **2** : ≥ 4/6 tokens (identifie off-by-one + donne le fix sans le `-1`)
- **1** : 2-3/6
- **0** : < 2/6

## Notes pour le juge

Python slicing est exclusive sur l'end. `items[start:end]` prend [start, end-1]. Donc `end = start + per_page` donne bien `per_page` items.
