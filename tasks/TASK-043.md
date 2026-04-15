# TASK-043 — multi-param-functions

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
    "authenticate_user"
  ]
}
```

## Scoring

- **2** : liste cohérente avec signatures (payload + user_id visibles, plusieurs fonctions nommées)
- **1** : réponse partielle
- **0** : absente

## Notes pour le juge

Les services déclarent leurs fonctions comme `def xxx(payload: dict, user_id: int = 0):` — toutes les publiques ont 2 paramètres. Baseline : grep/read sur plusieurs fichiers de 600+ lignes. TS : `get_functions` avec filtre arity.
