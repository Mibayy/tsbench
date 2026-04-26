# TASK-044 — code-gen-rate-limiter

**Catégorie** : code_generation
**Difficulté** : medium
**Artefact(s) lié(s)** : —
**Type de scoring** : `contains_all`

## Prompt (envoyé à l'agent)

> Implémente un rate limiter type **token bucket** en Python dans `packages/utils/rate_limiter.py`. Classe `TokenBucket(capacity: int, refill_rate: float)` avec méthode `consume(tokens: int = 1) -> bool` qui retourne True si assez de tokens. Le refill doit se faire lazy (calculé au moment de `consume`) via `time.monotonic()`. Donne le code complet.

## Réponse attendue

```json
{
  "expected_tokens": [
    "class TokenBucket",
    "capacity",
    "refill_rate",
    "def consume",
    "time.monotonic",
    "self.tokens",
    "min(",
    "packages/utils/rate_limiter.py"
  ]
}
```

## Scoring

- **2** : ≥ 7/8 tokens (token bucket correct avec lazy refill + cap)
- **1** : 4-6/8
- **0** : < 4/8

## Notes pour le juge

Erreurs classiques : utiliser `time.time()` (non-monotonic), oublier le cap `min(capacity, ...)` sur le refill, re-consommer des fractions de token.
