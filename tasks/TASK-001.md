# TASK-001 — find-function

**Catégorie** : localisation
**Difficulté** : easy
**Artefact(s) lié(s)** : CALLER-001
**Type de scoring** : `exact_match`

## Prompt (envoyé à l'agent)

> Dans ce projet, où est définie la fonction utilitaire `lonely_util` ? Donne-moi le fichier et la ligne.

## Réponse attendue

```json
{
  "file": "packages/utils/targeted.py",
  "symbol": "lonely_util",
  "line": 3
}
```

## Scoring

- **2** : fichier + symbole + ligne (±3) corrects
- **1** : fichier + symbole corrects, ligne hors tolérance
- **0** : symbole incorrect ou non trouvé

## Notes pour le juge

Symbole unique dans le projet — pas d'ambiguïté. Le fichier contient 4 fonctions utilitaires (lonely_util, small_util, medium_util, hub_util).
