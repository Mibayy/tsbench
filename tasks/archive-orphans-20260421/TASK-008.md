# TASK-008 — callers-exhaustive-3

**Catégorie** : dépendants
**Difficulté** : easy
**Artefact(s) lié(s)** : CALLER-002
**Type de scoring** : `set_match_strict`

## Prompt (envoyé à l'agent)

> Donne-moi la liste complète et exhaustive des fichiers qui appellent la fonction `small_util`. Je veux tous les call sites, pas un échantillon.

## Réponse attendue

```json
{
  "symbol": "small_util",
  "count": 3,
  "expected_files": [
    "apps/api/callers/caller_small_util_00.py",
    "apps/api/callers/caller_small_util_01.py",
    "apps/api/callers/caller_small_util_02.py"
  ]
}
```

## Scoring

- **2** : liste exactement égale à la liste attendue (F1 = 1.0)
- **1** : F1 ≥ 0.75 (un ou deux éléments manquants ou en trop)
- **0** : F1 < 0.75

## Notes pour le juge

Exactement 3 callers plantés. Test d'exhaustivité — un oubli = F1 < 1.
