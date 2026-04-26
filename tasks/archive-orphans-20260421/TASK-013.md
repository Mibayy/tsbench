# TASK-013 — chain-gamma

**Catégorie** : call_chain
**Difficulté** : medium
**Artefact(s) lié(s)** : CHAIN-003
**Type de scoring** : `chain_match`

## Prompt (envoyé à l'agent)

> À partir de la fonction `gamma_entry`, retrace la chaîne d'appels complète jusqu'à la fonction feuille (celle qui ne délègue plus à personne).

## Réponse attendue

```json
{
  "chain": [
    "gamma_entry",
    "gamma_middle",
    "gamma_inner",
    "gamma_leaf"
  ],
  "file": "apps/api/chains/gamma.py",
  "depth": 4
}
```

## Scoring

- **2** : chaîne complète dans le bon ordre
- **1** : tous les nœuds corrects mais ordre partiellement faux, ou un nœud manquant
- **0** : chaîne incorrecte ou incomplète (> 1 manquant)

## Notes pour le juge

Chaîne à 4 niveaux dans apps/api/chains/gamma.py. Ordre important.
