# TASK-063 — bug-fix-race-condition

**Catégorie** : bug_fixing
**Difficulté** : hard
**Artefact(s) lié(s)** : —
**Type de scoring** : `contains_all`

## Prompt (envoyé à l'agent)

> Ce compteur thread-safe ne l'est pas vraiment :
>
> ```python
> class Counter:
>     def __init__(self):
>         self.value = 0
>     def increment(self):
>         current = self.value
>         self.value = current + 1
> ```
>
> Deux threads peuvent lire la même `current` et écraser. Donne le fix avec `threading.Lock`. Mentionne aussi une alternative lock-free avec `itertools.count` ou `threading.local`. Précise le trade-off.

## Réponse attendue

```json
{
  "expected_tokens": [
    "race condition",
    "threading.Lock",
    "with self._lock",
    "atomic",
    "itertools.count",
    "__next__",
    "increment"
  ]
}
```

## Scoring

- **2** : ≥ 6/7 tokens (lock correct + mention alternative)
- **1** : 3-5/7
- **0** : < 3/7

## Notes pour le juge

Piège : mettre le lock mais oublier de l'utiliser sur le read seul. Ou utiliser `self.value += 1` sans lock en pensant que c'est atomique (ne l'est pas en Python).
