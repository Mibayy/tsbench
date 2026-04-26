# TASK-024 — list-auth-public-functions

**Catégorie** : heavy_read
**Difficulté** : medium
**Artefact(s) lié(s)** :
**Type de scoring** : `contains_all`

## Prompt (envoyé à l'agent)

> Liste toutes les fonctions publiques (non-underscore) de `apps/api/services/auth.py` avec leur signature complète (nom + paramètres). Donne-moi la liste exhaustive, pas juste les premières.

## Réponse attendue

```json
{
  "must_contain": [
    "authenticate_user",
    "issue_token",
    "revoke_token",
    "hash_password",
    "verify_password"
  ]
}
```

## Scoring

- **2** : les 5 fonctions publiques listées avec signature
- **1** : ≥3 fonctions
- **0** : <3

## Notes pour le juge

Fichier de 614 lignes avec ~30 fonctions dont 5 publiques principales. Baseline : Read du fichier entier. TS : `get_functions` sur le fichier.
