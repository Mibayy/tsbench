# TASK-045 — code-gen-retry-backoff

**Catégorie** : code_generation
**Difficulté** : medium
**Artefact(s) lié(s)** : —
**Type de scoring** : `contains_all`

## Prompt (envoyé à l'agent)

> Implémente un décorateur Python `@retry(max_attempts=3, base_delay=0.5, exceptions=(Exception,))` dans `packages/utils/retry.py`. Il doit :
> - Réessayer la fonction décorée jusqu'à max_attempts fois
> - Exponential backoff : delay = base_delay * 2^(attempt-1)
> - Ajouter un jitter (random entre 0 et delay*0.1)
> - N'attraper que les `exceptions` passées
> - Laisser lever la dernière exception si toutes les tentatives échouent

## Réponse attendue

```json
{
  "expected_tokens": [
    "def retry",
    "max_attempts",
    "base_delay",
    "exceptions",
    "functools.wraps",
    "time.sleep",
    "random",
    "** attempt",
    "packages/utils/retry.py"
  ]
}
```

## Scoring

- **2** : ≥ 7/9 tokens
- **1** : 4-6/9
- **0** : < 4/9

## Notes pour le juge

Exponential backoff = multiplier par 2^n (pas linéaire). Jitter évite thundering herd. `functools.wraps` préserve metadata.
