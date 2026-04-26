# TASK-073 — refactor-replace-loop-comprehension

**Catégorie** : refactoring
**Difficulté** : easy
**Artefact(s) lié(s)** : —
**Type de scoring** : `contains_all`

## Prompt (envoyé à l'agent)

> Ce code peut être exprimé en comprehension :
>
> ```python
> active_emails = []
> for user in users:
>     if user.is_active and user.email:
>         active_emails.append(user.email.lower())
> ```
>
> Transforme-le en list comprehension. Donne aussi la variante dict (dict comprehension : `user.id → user.email.lower()`) et set. Note : à quel moment la loop explicite reste préférable ? (hint : side effects, break/continue, logging).

## Réponse attendue

```json
{
  "expected_tokens": [
    "comprehension",
    "[user.email.lower()",
    "for user in users",
    "if user.is_active",
    "and user.email",
    "{user.id:",
    "side effects"
  ]
}
```

## Scoring

- **2** : ≥ 5/7 tokens (3 variantes + trade-off mentionné)
- **1** : 3-4/7
- **0** : < 3/7

## Notes pour le juge

Piège : compactifier en one-liner illisible (triple filtre). Les comprehensions doivent rester lisibles. Mention explicite que side-effects (log, write) = loop préférable.
