# TASK-018 — dup-detection

**Catégorie** : debug
**Difficulté** : hard
**Artefact(s) lié(s)** : DUP-001, DUP-002, DUP-003
**Type de scoring** : `set_match_strict`

## Prompt (envoyé à l'agent)

> Y a-t-il des fonctions sémantiquement dupliquées dans ce projet ? Si oui, cite les paires que tu trouves.

## Réponse attendue

```json
{
  "expected_pairs": [
    [
      {
        "file": "apps/api/utils/strings.py",
        "symbol": "slugify"
      },
      {
        "file": "packages/utils/slug_copy.py",
        "symbol": "to_slug"
      }
    ],
    [
      {
        "file": "apps/api/utils/dates.py",
        "symbol": "start_of_day"
      },
      {
        "file": "packages/utils/date_copy.py",
        "symbol": "day_start"
      }
    ]
  ],
  "count": 2
}
```

## Scoring

- **2** : liste exactement égale à la liste attendue (F1 = 1.0)
- **1** : F1 ≥ 0.75 (un ou deux éléments manquants ou en trop)
- **0** : F1 < 0.75

## Notes pour le juge

2 paires hash-identiques : slugify/to_slug, start_of_day/day_start.
paginate/paginate_also retirées : default values différents = pas hash-identiques.
