# TASK-002 — find-callers

**Catégorie** : localisation
**Difficulté** : medium
**Artefact(s) lié(s)** : CALLER-002
**Type de scoring** : `set_match_strict`

## Prompt (envoyé à l'agent)

> Liste tous les endroits qui appellent `small_util`. Je veux une liste exhaustive de fichiers.

## Réponse attendue

```json
{
  "symbol": "small_util",
  "expected_files": [
    "apps/api/callers/caller_small_util_00.py",
    "apps/api/callers/caller_small_util_01.py",
    "apps/api/callers/caller_small_util_02.py"
  ],
  "count": 3
}
```

## Scoring

- **2** : liste exactement égale à la liste attendue (F1 = 1.0)
- **1** : F1 ≥ 0.75 (un ou deux éléments manquants ou en trop)
- **0** : F1 < 0.75

## Notes pour le juge

3 callers exactement dans apps/api/callers/caller_small_util_*.py. Pas de faux positifs attendus.
