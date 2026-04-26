# TASK-007 -- entry-points

**Categorie** : navigation
**Difficulte** : medium
**Artefact(s) lie(s)** :
**Type de scoring** : `contains_all`

## Prompt (envoye a l'agent)

> Quels sont les points d'entree du projet tsbench ? Identifie les fonctions qui sont des racines du graphe d'appels (appelees mais n'ayant pas d'appelant dans le code).

## Réponse attendue

```json
{
  "must_contain": [
    "main",
    "create_app"
  ]
}
```

## Scoring

- **2** : entry points principaux identifies correctement
- **1** : >=1 entry point identifie
- **0** : aucun

## Notes pour le juge

Teste `get_entry_points`. Identification des racines du graphe d'appels du projet.
