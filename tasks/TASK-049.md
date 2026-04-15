# TASK-049 -- call-chain-deep

**Categorie** : call_chain
**Difficulte** : hard
**Artefact(s) lie(s)** : CHAIN-001
**Type de scoring** : `chain_match`

## Prompt (envoye a l'agent)

> Donne le chemin d'appel exact entre `alpha_entry` et `alpha_leaf` -- pas leurs dependances directes, le chemin complet. Utilise exclusivement get_call_chain pour trouver la chaine.

## Réponse attendue

```json
{
  "chain": [
    "alpha_entry",
    "alpha_middle",
    "alpha_inner",
    "alpha_leaf"
  ]
}
```

## Scoring

- **2** : chaine exacte alpha_entry -> alpha_middle -> alpha_inner -> alpha_leaf
- **1** : chaine partielle (>=2 maillons corrects)
- **0** : pas de chaine ou chaine incorrecte

## Notes pour le juge

Teste `get_call_chain` avec disallowed get_dependencies/get_dependents pour forcer le BFS natif plutot que navigation manuelle du graphe.
