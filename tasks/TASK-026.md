# TASK-026 — cycle-detection

**Catégorie** : audit
**Difficulté** : medium
**Artefact(s) lié(s)** : CYCLE-001, CYCLE-002
**Type de scoring** : `set_match_strict`

## Prompt (envoyé à l'agent)

> Y a-t-il des dépendances circulaires (import cycles) dans ce projet ? Si oui, cite-les.

## Réponse attendue

```json
{
  "has_cycles": true,
  "expected_cycles": [
    [
      "apps/api/cycles/mod_a.py",
      "apps/api/cycles/mod_b.py"
    ],
    [
      "apps/api/cycles/mod_x.py",
      "apps/api/cycles/mod_y.py",
      "apps/api/cycles/mod_z.py"
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

2 cycles plantés : mod_a↔mod_b et mod_x→mod_y→mod_z→mod_x.
