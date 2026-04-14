# TASK-014 — breaking-signature

**Catégorie** : impact
**Difficulté** : hard
**Artefact(s) lié(s)** : CALLER-004
**Type de scoring** : `impact_set`

## Prompt (envoyé à l'agent)

> Je compte changer la signature de la fonction `hub_util` dans `packages/utils/targeted.py` pour qu'elle prenne un seul argument `context: dict` au lieu de `payload: dict`. Liste exhaustivement ce qui casse ailleurs dans le projet.

## Réponse attendue

```json
{
  "symbol": "hub_util",
  "file": "packages/utils/targeted.py",
  "affected_files": [
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
  ],
  "affected_count": 20
}
```

## Scoring

- **2** : liste exhaustive des dépendants (précision + rappel = 1.0)
- **1** : rappel ≥ 0.75 (quelques oublis tolérés)
- **0** : rappel < 0.75

## Notes pour le juge

20 callers — test stress de l'analyse d'impact transitive. Aucun call site ne doit être oublié.
