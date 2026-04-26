# TASK-061 — bug-fix-null-deref

**Catégorie** : bug_fixing
**Difficulté** : easy
**Artefact(s) lié(s)** : —
**Type de scoring** : `contains_all`

## Prompt (envoyé à l'agent)

> Ce code lève une `AttributeError` en prod quand `user` n'existe pas en DB :
>
> ```python
> def get_user_email(user_id: int) -> str:
>     user = db.query(User).filter_by(id=user_id).first()
>     return user.email.lower()
> ```
>
> Identifie le bug et donne le fix (doit être robuste : retourner `None` si user ou email absent, ne pas lever). Précise si une validation doit lever à la place.

## Réponse attendue

```json
{
  "expected_tokens": [
    "user is None",
    "return None",
    "user.email",
    "NotFoundError",
    "if not user",
    "AttributeError"
  ]
}
```

## Scoring

- **2** : ≥ 4/6 tokens (guard + return None ou raise NotFoundError)
- **1** : 2-3/6 (guard partiel)
- **0** : < 2/6

## Notes pour le juge

Deux niveaux : user None (query miss) ET user.email None (champ null en DB). Réponse 2/2 doit évoquer au moins le premier. Soit `return None`, soit `raise NotFoundError` est acceptable selon la sémantique demandée par le reste de l'API.
