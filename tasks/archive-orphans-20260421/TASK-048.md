# TASK-048 -- file-dependents-reverse

**Categorie** : navigation
**Difficulte** : medium
**Artefact(s) lie(s)** :
**Type de scoring** : `set_match_loose`

## Prompt (envoye a l'agent)

> Quels fichiers importent `apps/api/config.py` ? Liste tous les fichiers qui dependent de ce module.

## Réponse attendue

```json
{
  "expected_files": [
    "apps/api/main.py",
    "apps/api/services/audit.py",
    "apps/api/services/auth.py",
    "apps/api/services/billing.py",
    "apps/api/services/exports.py",
    "apps/api/services/integrations.py",
    "apps/api/services/members.py",
    "apps/api/services/notifications.py",
    "apps/api/services/reports.py",
    "apps/api/services/sessions.py",
    "apps/api/services/webhooks.py",
    "apps/api/utils/logging.py",
    "apps/api/utils/pagination.py"
  ]
}
```

## Scoring

- **2** : >=12/13 fichiers identifies
- **1** : >=6 fichiers identifies
- **0** : <6

## Notes pour le juge

Teste `get_file_dependents`. 13 dependants reels. Le baseline devrait grep `from.*config import` dans tout le projet.
