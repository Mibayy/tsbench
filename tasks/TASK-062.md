# TASK-062 — bug-fix-sql-injection

**Catégorie** : bug_fixing
**Difficulté** : hard
**Artefact(s) lié(s)** : —
**Type de scoring** : `contains_all`

## Prompt (envoyé à l'agent)

> Code en revue :
>
> ```python
> def search_orders(status: str, customer: str):
>     q = f"SELECT * FROM orders WHERE status = '{status}' AND customer = '{customer}'"
>     return db.execute(q).fetchall()
> ```
>
> Quelles vulnérabilités ? Donne le fix. Précise aussi ce que l'attaquant pourrait faire concrètement avec un payload malicieux dans `customer`.

## Réponse attendue

```json
{
  "expected_tokens": [
    "SQL injection",
    "parameterized",
    "execute(",
    "?",
    "%s",
    "fetchall",
    "status",
    "customer",
    "UNION"
  ]
}
```

## Scoring

- **2** : ≥ 7/9 tokens (identifie SQLi + propose paramétrisée + cite un exemple concret)
- **1** : 4-6/9
- **0** : < 4/9

## Notes pour le juge

Le fix doit utiliser placeholders `?` (sqlite), `%s` (psycopg2) ou bind params (SQLAlchemy text()). Une réponse qui suggère juste "escape les quotes" = 0.
