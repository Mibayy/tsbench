# TASK-010 — callers-exhaustive-20

**Catégorie** : dépendants
**Difficulté** : hard
**Artefact(s) lié(s)** : CALLER-004
**Type de scoring** : `set_match_strict`

## Prompt (envoyé à l'agent)

> Donne-moi la liste complète et exhaustive des fichiers qui appellent la fonction `hub_util`. Je veux tous les call sites, pas un échantillon.

## Réponse attendue

```json
{
  "symbol": "hub_util",
  "count": 20,
  "expected_files": [
    "apps/api/callers/caller_hub_util_00.py",
    "apps/api/callers/caller_hub_util_01.py",
    "apps/api/callers/caller_hub_util_02.py",
    "apps/api/callers/caller_hub_util_03.py",
    "apps/api/callers/caller_hub_util_04.py",
    "apps/api/callers/caller_hub_util_05.py",
    "apps/api/callers/caller_hub_util_06.py",
    "apps/api/callers/caller_hub_util_07.py",
    "apps/api/callers/caller_hub_util_08.py",
    "apps/api/callers/caller_hub_util_09.py",
    "apps/api/callers/caller_hub_util_10.py",
    "apps/api/callers/caller_hub_util_11.py",
    "apps/api/callers/caller_hub_util_12.py",
    "apps/api/callers/caller_hub_util_13.py",
    "apps/api/callers/caller_hub_util_14.py",
    "apps/api/callers/caller_hub_util_15.py",
    "apps/api/callers/caller_hub_util_16.py",
    "apps/api/callers/caller_hub_util_17.py",
    "apps/api/callers/caller_hub_util_18.py",
    "apps/api/callers/caller_hub_util_19.py"
  ]
}
```

## Scoring

- **2** : liste exactement égale à la liste attendue (F1 = 1.0)
- **1** : F1 ≥ 0.75 (un ou deux éléments manquants ou en trop)
- **0** : F1 < 0.75

## Notes pour le juge

Exactement 20 callers plantés. Test d'exhaustivité — un oubli = F1 < 1.
