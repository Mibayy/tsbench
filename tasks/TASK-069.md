# TASK-069 — refactor-inline-variable

**Catégorie** : refactoring
**Difficulté** : easy
**Artefact(s) lié(s)** : —
**Type de scoring** : `contains_all`

## Prompt (envoyé à l'agent)

> Ce code a des variables intermédiaires inutiles :
>
> ```python
> def get_user_display(user):
>     full_name = user.first_name + " " + user.last_name
>     display = full_name.strip()
>     return display
> ```
>
> Refactor en inlinant les variables temporaires. Justifie pourquoi c'est plus lisible ici. Précise à quel moment l'inlining devient DÉFAUT (hint: debug / named intent).

## Réponse attendue

```json
{
  "expected_tokens": [
    "return",
    "strip()",
    "inline",
    "intermediate",
    "readability",
    "f-string",
    "debug"
  ]
}
```

## Scoring

- **2** : ≥ 5/7 tokens (code inliné + explique trade-off debug)
- **1** : 3-4/7
- **0** : < 3/7

## Notes pour le juge

Code final idéal : `return f"{user.first_name} {user.last_name}".strip()`. Le mini-essai sur quand NE PAS inliner est le vrai test (gardez une var si elle porte un nom métier `total_after_tax` par ex).
