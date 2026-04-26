# TASK-057 — code-gen-json-diff

**Catégorie** : code_generation
**Difficulté** : hard
**Artefact(s) lié(s)** : —
**Type de scoring** : `contains_all`

## Prompt (envoyé à l'agent)

> Implémente `json_diff(a: dict, b: dict) -> dict` dans `packages/utils/json_diff.py`. Le résultat contient 3 clés : `added` (dans b pas dans a), `removed` (dans a pas dans b), `changed` (présent dans les deux avec valeurs différentes, listé comme `{key: {"before": ..., "after": ...}}`). Supporte la récursion sur dicts imbriqués : si a[k] et b[k] sont tous deux dicts, diff récursif. Les paths imbriqués sont représentés par une clé dotted (ex `"user.name"`).

## Réponse attendue

```json
{
  "expected_tokens": [
    "def json_diff",
    "added",
    "removed",
    "changed",
    "isinstance",
    "dict",
    "before",
    "after",
    "packages/utils/json_diff.py"
  ]
}
```

## Scoring

- **2** : ≥ 7/9 tokens
- **1** : 4-6/9
- **0** : < 4/9

## Notes pour le juge

Récursion sur dict → flattening avec clé dotted. Piège : ne pas traiter le cas `list` (bonus si c'est fait proprement).
