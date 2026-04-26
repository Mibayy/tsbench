# TASK-025 — multi-param-functions

**Catégorie** : heavy_read
**Difficulté** : hard
**Artefact(s) lié(s)** :
**Type de scoring** : `contains_all`

## Prompt (envoyé à l'agent)

> Dans le dossier `apps/api/services/`, identifie les fonctions publiques (non-underscore, non-internal) qui acceptent plus d'un paramètre. Donne-moi leur nom et leur signature, file par file.

## Réponse attendue

```json
{
  "must_contain": [
    "payload",
    "user_id",
    "calculate_invoice",
    "apply_discount"
  ]
}
```

## Scoring

- **2** : liste cohérente avec signatures (payload + user_id visibles, plusieurs fonctions nommées)
- **1** : réponse partielle
- **0** : absente

## Notes pour le juge

Les services déclarent leurs fonctions publiques comme `def xxx(payload: dict, user_id: int = 0):` — la plupart ont 2 paramètres (exception : `authenticate_user` a été simplifié à 1 param via BREAK-002). Baseline : grep/read sur plusieurs fichiers de 600+ lignes. TS : `get_functions` avec filtre arity.
