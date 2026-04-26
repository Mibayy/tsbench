# TASK-068 — refactor-extract-function

**Catégorie** : refactoring
**Difficulté** : medium
**Artefact(s) lié(s)** : —
**Type de scoring** : `contains_all`

## Prompt (envoyé à l'agent)

> La fonction `calculate_invoice` dans `apps/api/services/billing.py` contient un bloc de ~17 lignes de calcul qui calcule des valeurs intermédiaires (`x_0`..`x_17`) sans lien avec le vrai calcul de facture. Ce bloc est dupliqué dans d'autres fonctions du même fichier.
>
> Extrais ce bloc en une fonction helper privée `_compute_ladder_values()` dans le même fichier, qui retourne un dict des valeurs. Modifie `calculate_invoice` pour l'appeler. Donne le code du helper + l'insertion dans `calculate_invoice`.

## Réponse attendue

```json
{
  "expected_tokens": [
    "def _compute_ladder_values",
    "return {",
    "calculate_invoice",
    "_compute_ladder_values()",
    "apps/api/services/billing.py",
    "x_0",
    "x_17"
  ]
}
```

## Scoring

- **2** : ≥ 6/7 tokens (helper extrait + appel modifié)
- **1** : 3-5/7
- **0** : < 3/7

## Notes pour le juge

Refactor classique : extract method. Accepté sans tokens exacts si la solution propose un helper parametré avec moins de noise code. L'important : 1 def helper + 1 appel dans la fonction modifiée.
