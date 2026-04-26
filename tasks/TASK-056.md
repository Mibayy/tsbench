# TASK-056 — code-gen-circuit-breaker

**Catégorie** : code_generation
**Difficulté** : hard
**Artefact(s) lié(s)** : —
**Type de scoring** : `contains_all`

## Prompt (envoyé à l'agent)

> Implémente une classe `CircuitBreaker(failure_threshold: int = 5, reset_timeout: float = 30.0)` dans `packages/utils/circuit.py`. 3 états : CLOSED, OPEN, HALF_OPEN. Méthode `call(fn, *args, **kwargs)` :
> - CLOSED → exécute, si >= threshold failures consécutives → OPEN
> - OPEN → lève `CircuitOpenError` immédiatement ; après `reset_timeout` → HALF_OPEN
> - HALF_OPEN → 1 tentative ; succès → CLOSED, échec → OPEN
>
> Thread-safe via `threading.Lock`.

## Réponse attendue

```json
{
  "expected_tokens": [
    "class CircuitBreaker",
    "CLOSED",
    "OPEN",
    "HALF_OPEN",
    "CircuitOpenError",
    "failure_threshold",
    "reset_timeout",
    "threading.Lock",
    "packages/utils/circuit.py"
  ]
}
```

## Scoring

- **2** : ≥ 7/9 tokens
- **1** : 4-6/9
- **0** : < 4/9

## Notes pour le juge

Les 3 états + transition HALF_OPEN sont essentiels. Oublier HALF_OPEN = circuit breaker incomplet.
