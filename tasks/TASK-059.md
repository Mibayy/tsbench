# TASK-059 — code-gen-date-range-expander

**Catégorie** : code_generation
**Difficulté** : medium
**Artefact(s) lié(s)** : —
**Type de scoring** : `contains_all`

## Prompt (envoyé à l'agent)

> Implémente `expand_date_range(start: str, end: str, *, step: str = "day") -> list[str]` dans `packages/utils/date_range.py`. `start` et `end` au format ISO `YYYY-MM-DD`. `step` ∈ {"day", "week", "month"}. Retourne la liste des dates (format ISO string) depuis `start` jusqu'à `end` inclus. Utilise `datetime.date`, `timedelta` pour day/week, et `dateutil.relativedelta` pour month. Lève `ValueError` si end < start ou step invalide.

## Réponse attendue

```json
{
  "expected_tokens": [
    "def expand_date_range",
    "from datetime import",
    "timedelta",
    "relativedelta",
    "isoformat",
    "ValueError",
    "step",
    "packages/utils/date_range.py"
  ]
}
```

## Scoring

- **2** : ≥ 6/8 tokens
- **1** : 3-5/8
- **0** : < 3/8

## Notes pour le juge

`relativedelta(months=1)` pour incrément mensuel (timedelta ne gère pas les mois). Alternative acceptée : calcul manuel du mois suivant.
