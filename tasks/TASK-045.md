# TASK-045 — auth-importers

**Catégorie** : heavy_read
**Difficulté** : medium
**Artefact(s) lié(s)** :
**Type de scoring** : `list_f1`

## Prompt (envoyé à l'agent)

> Quels fichiers Python du projet importent quelque chose depuis `apps.api.services.auth` ? Donne la liste complète des fichiers importateurs.

## Réponse attendue

```json
{
  "expected_files": [
    "apps/api/routers/auth.py",
    "tests/test_auth.py"
  ]
}
```

## Scoring

- **2** : les 2 fichiers importateurs cités (recall ≥ 0.95)
- **1** : 1 fichier sur 2 (recall = 0.5)
- **0** : aucun fichier correct

## Notes pour le juge

Vérité-terrain vérifiée par grep sur la fixture : deux fichiers importent `from apps.api.services import auth`. NB : `apps/api/models/__init__.py` importe `from .auth` mais cible `apps/api/models/auth.py` — pas le service — et doit être exclu. Baseline : grep récursif. TS : `get_file_dependents` sur `apps/api/services/auth.py`.
