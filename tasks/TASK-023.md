# TASK-023 — breaking-detection

**Catégorie** : review
**Difficulté** : medium
**Artefact(s) lié(s)** : BREAK-001, BREAK-002, BREAK-003, BREAK-004, BREAK-005, BREAK-006
**Type de scoring** : `set_match_strict`

## Prompt (envoyé à l'agent)

> Y a-t-il des breaking changes d'API entre v1 et v2 ? Si oui, lesquels exactement ?

## Réponse attendue

```json
{
  "has_breaking": true,
  "expected_breaks": [
    "BREAK-001",
    "BREAK-002",
    "BREAK-003",
    "BREAK-004",
    "BREAK-005",
    "BREAK-006"
  ],
  "expected_count": 6
}
```

## Scoring

- **2** : liste exactement égale à la liste attendue (F1 = 1.0)
- **1** : F1 ≥ 0.75 (un ou deux éléments manquants ou en trop)
- **0** : F1 < 0.75

## Notes pour le juge

Les 6 BREAK-* doivent être cités nommément (ou par description équivalente).
