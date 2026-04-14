# TASK-009 — callers-exhaustive-8

**Catégorie** : dépendants
**Difficulté** : medium
**Artefact(s) lié(s)** : CALLER-003
**Type de scoring** : `set_match_strict`

## Prompt (envoyé à l'agent)

> Donne-moi la liste complète et exhaustive des fichiers qui appellent la fonction `medium_util`. Je veux tous les call sites, pas un échantillon.

## Réponse attendue

```json
{
  "symbol": "medium_util",
  "count": 8,
  "expected_files": [
    "apps/api/callers/caller_medium_util_00.py",
    "apps/api/callers/caller_medium_util_01.py",
    "apps/api/callers/caller_medium_util_02.py",
    "apps/api/callers/caller_medium_util_03.py",
    "apps/api/callers/caller_medium_util_04.py",
    "apps/api/callers/caller_medium_util_05.py",
    "apps/api/callers/caller_medium_util_06.py",
    "apps/api/callers/caller_medium_util_07.py"
  ]
}
```

## Scoring

- **2** : liste exactement égale à la liste attendue (F1 = 1.0)
- **1** : F1 ≥ 0.75 (un ou deux éléments manquants ou en trop)
- **0** : F1 < 0.75

## Notes pour le juge

Exactement 8 callers plantés. Test d'exhaustivité — un oubli = F1 < 1.
