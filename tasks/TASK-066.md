# TASK-066 — bug-fix-timezone

**Catégorie** : bug_fixing
**Difficulté** : medium
**Artefact(s) lié(s)** : —
**Type de scoring** : `contains_all`

## Prompt (envoyé à l'agent)

> Ce code dit "la commande a expiré" même sur des timestamps qui ne devraient pas :
>
> ```python
> def is_expired(created_at: datetime, ttl_hours: int = 24) -> bool:
>     return datetime.now() > created_at + timedelta(hours=ttl_hours)
> ```
>
> Sachant que `created_at` vient de la DB en UTC (aware datetime avec tzinfo=UTC), identifie le bug et propose un fix robuste. Mentionne l'erreur précise que lève Python dans certains cas.

## Réponse attendue

```json
{
  "expected_tokens": [
    "datetime.now()",
    "naive",
    "aware",
    "tzinfo",
    "datetime.now(timezone.utc)",
    "TypeError",
    "utcnow"
  ]
}
```

## Scoring

- **2** : ≥ 5/7 tokens (identifie le mix naive/aware + TypeError + fix avec tz)
- **1** : 3-4/7
- **0** : < 3/7

## Notes pour le juge

`datetime.now()` retourne naive ; comparaison naive/aware → `TypeError: can't compare offset-naive and offset-aware datetimes`. Fix : `datetime.now(timezone.utc)` ou tout migrer en naive UTC.
