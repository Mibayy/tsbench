# TASK-011 — chain-alpha

**Catégorie** : call_chain
**Difficulté** : medium
**Artefact(s) lié(s)** : CHAIN-001
**Type de scoring** : `chain_match`

## Prompt (envoyé à l'agent)

> À partir de la fonction `alpha_entry`, retrace la chaîne d'appels complète jusqu'à la fonction feuille (celle qui ne délègue plus à personne).

## Réponse attendue

```json
{
  "chain": [
    "alpha_entry",
    "alpha_middle",
    "alpha_inner",
    "alpha_leaf"
  ],
  "file": "apps/api/chains/alpha.py",
  "depth": 4
}
```

## Scoring

- **2** : chaîne complète dans le bon ordre
- **1** : tous les nœuds corrects mais ordre partiellement faux, ou un nœud manquant
- **0** : chaîne incorrecte ou incomplète (> 1 manquant)

## Notes pour le juge

Chaîne à 4 niveaux dans apps/api/chains/alpha.py. Ordre important.
