# TASK-050 — code-gen-debounce

**Catégorie** : code_generation
**Difficulté** : medium
**Artefact(s) lié(s)** : —
**Type de scoring** : `contains_all`

## Prompt (envoyé à l'agent)

> Implémente un décorateur `@debounce(wait: float)` dans `packages/utils/debounce.py`. Si la fonction décorée est rappelée avant `wait` secondes, le premier appel est annulé et un nouveau timer démarre. Utilise `threading.Timer`. Donne le code complet avec gestion thread-safe (lock).

## Réponse attendue

```json
{
  "expected_tokens": [
    "def debounce",
    "wait",
    "threading.Timer",
    "cancel()",
    "Lock",
    "functools.wraps",
    "packages/utils/debounce.py"
  ]
}
```

## Scoring

- **2** : ≥ 6/7 tokens
- **1** : 3-5/7
- **0** : < 3/7

## Notes pour le juge

Piège : oublier le lock → race condition entre cancel et restart. Ou utiliser `asyncio` quand le prompt demande threading.
