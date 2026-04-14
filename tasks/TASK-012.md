# TASK-012 — chain-beta

**Catégorie** : call_chain
**Difficulté** : medium
**Artefact(s) lié(s)** : CHAIN-002
**Type de scoring** : `chain_match`

## Prompt (envoyé à l'agent)

> À partir de la fonction `beta_entry`, retrace la chaîne d'appels complète jusqu'à la fonction feuille (celle qui ne délègue plus à personne).

## Réponse attendue

```json
{
  "chain": [
    "beta_entry",
    "beta_middle",
    "beta_inner",
    "beta_leaf"
  ],
  "file": "apps/api/chains/beta.py",
  "depth": 4
}
```

## Scoring

- **2** : chaîne complète dans le bon ordre
- **1** : tous les nœuds corrects mais ordre partiellement faux, ou un nœud manquant
- **0** : chaîne incorrecte ou incomplète (> 1 manquant)

## Notes pour le juge

Chaîne à 4 niveaux dans apps/api/chains/beta.py. Ordre important.
