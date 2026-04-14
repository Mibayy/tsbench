# TASK-015 — file-impact

**Catégorie** : impact
**Difficulté** : medium
**Artefact(s) lié(s)** : CYCLE-001
**Type de scoring** : `set_match_loose`

## Prompt (envoyé à l'agent)

> Je m'apprête à modifier `apps/api/cycles/mod_a.py`. Quels fichiers du projet sont susceptibles d'être affectés en aval (directement ou transitivement) ?

## Réponse attendue

```json
{
  "source": "apps/api/cycles/mod_a.py",
  "min_expected_downstream": [
    "apps/api/cycles/mod_b.py"
  ],
  "hint": "cycle présent entre mod_a et mod_b"
}
```

## Scoring

- **2** : la réponse contient au moins N éléments corrects parmi ceux attendus
- **1** : au moins la moitié des éléments attendus sont cités
- **0** : aucun élément correct

## Notes pour le juge

Cycle planté : mod_a ↔ mod_b. Le bon agent détecte l'impact circulaire.
