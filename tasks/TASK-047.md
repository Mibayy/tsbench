# TASK-047 -- file-deps-graph

**Categorie** : navigation
**Difficulte** : easy
**Artefact(s) lie(s)** :
**Type de scoring** : `set_match_strict`

## Prompt (envoye a l'agent)

> Quels fichiers sont importes directement par `apps/api/services/auth.py` ? Liste tous les imports locaux (pas les packages tiers).

## Réponse attendue

```json
{
  "expected_files": [
    "apps/api/config.py",
    "apps/api/db.py",
    "apps/api/models/auth.py",
    "apps/api/utils/errors.py",
    "apps/api/utils/logging.py"
  ]
}
```

## Scoring

- **2** : les 5 fichiers identifies
- **1** : >=3 fichiers identifies
- **0** : <3

## Notes pour le juge

Teste `get_file_dependencies`. Le baseline devrait lire le fichier et parser les imports manuellement.
