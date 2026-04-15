# TASK-044 — dispatch-webhook-chain

**Catégorie** : heavy_read
**Difficulté** : hard
**Artefact(s) lié(s)** :
**Type de scoring** : `chain_match`

## Prompt (envoyé à l'agent)

> Trace le call chain complet de la fonction `dispatch_webhook` dans `apps/api/services/webhooks.py` : toutes les fonctions qu'elle appelle directement ou indirectement, y compris les accès à la base de données.

## Réponse attendue

```json
{
  "chain": [
    "dispatch_webhook",
    "webhooks_admin_db"
  ]
}
```

## Scoring

- **2** : entrypoint + helper DB + au moins un helper interne cités
- **1** : entrypoint + au moins un helper
- **0** : seulement dispatch_webhook ou erreur

## Notes pour le juge

Baseline : read de webhooks.py (614 lignes) + potentiellement d'autres fichiers. TS : `get_call_chain` ou `get_dependencies` sur le symbole.
