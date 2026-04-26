# TASK-043 — code-gen-lru-cache

**Catégorie** : code_generation
**Difficulté** : medium
**Artefact(s) lié(s)** : —
**Type de scoring** : `contains_all`

## Prompt (envoyé à l'agent)

> Implémente une classe `LRUCache` en Python avec `get(key)`, `put(key, value)` et capacité max fixée à la construction. Utilise `collections.OrderedDict`. Les accès (get, put) doivent déplacer la clé en queue pour LRU. `get` retourne `None` si absent. Donne le code complet de la classe dans un fichier `packages/utils/lru.py`.

## Réponse attendue

```json
{
  "expected_tokens": [
    "class LRUCache",
    "OrderedDict",
    "def get",
    "def put",
    "move_to_end",
    "popitem",
    "capacity",
    "packages/utils/lru.py"
  ]
}
```

## Scoring

- **2** : ≥ 7/8 tokens (implémentation correcte avec OrderedDict + LRU eviction)
- **1** : 4-6/8
- **0** : < 4/8

## Notes pour le juge

LRU correct implique move_to_end sur get+put et popitem(last=False) pour évincer. Manquer `move_to_end` sur `get` est une erreur classique.
