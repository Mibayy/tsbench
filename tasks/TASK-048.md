# TASK-048 — code-gen-pagination-helper

**Catégorie** : code_generation
**Difficulté** : easy
**Artefact(s) lié(s)** : —
**Type de scoring** : `contains_all`

## Prompt (envoyé à l'agent)

> Écris une fonction `paginate(items: list, page: int, per_page: int) -> dict` dans `packages/utils/paginate.py`. Retourne un dict `{"items": [...], "page": int, "per_page": int, "total": int, "total_pages": int, "has_next": bool, "has_prev": bool}`. `page` est 1-indexé. Gère les edge cases (page 0, page > total_pages, per_page ≤ 0 → lever `ValueError`).

## Réponse attendue

```json
{
  "expected_tokens": [
    "def paginate",
    "page: int",
    "per_page: int",
    "total_pages",
    "has_next",
    "has_prev",
    "ValueError",
    "math.ceil",
    "packages/utils/paginate.py"
  ]
}
```

## Scoring

- **2** : ≥ 7/9 tokens
- **1** : 4-6/9
- **0** : < 4/9

## Notes pour le juge

`math.ceil(total / per_page)` pour total_pages, ou équivalent avec division entière + 1. Erreur classique : off-by-one sur `has_next` (oublier `page >= total_pages`).
