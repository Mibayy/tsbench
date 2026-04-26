# TASK-020 — bug-fix-discount-validation

**Catégorie** : bug_fixing
**Difficulté** : medium
**Artefact(s) lié(s)** : —
**Type de scoring** : `contains_all`

## Prompt (envoyé à l'agent)

> La fonction `apply_discount` dans `apps/api/services/billing.py` reçoit un `payload` qui contient (entre autres) une clé `discount_percent` (float). Aujourd'hui elle n'effectue aucune validation sur cette valeur — ce qui laisse passer des pourcentages négatifs ou supérieurs à 100.
>
> 1. Identifie le problème précis (quelle valeur n'est pas validée)
> 2. Écris le bloc de validation à insérer au tout début de la fonction (après la docstring, avant les x_0...)
> 3. La validation doit lever une `ValidationError` (déjà importée en haut du fichier) si le pourcentage est absent, < 0 ou > 100
> 4. Indique la ligne d'insertion

## Réponse attendue

```json
{
  "expected_tokens": [
    "discount_percent",
    "ValidationError",
    "payload.get",
    "< 0",
    "> 100",
    "apps/api/services/billing.py"
  ]
}
```

## Scoring

- **2** : ≥ 5/6 tokens présents (bug identifié + fix complet + localisation)
- **1** : 3-4/6 (bug identifié mais fix partiel)
- **0** : < 3/6

## Notes pour le juge

Bug-fix classique nécessitant : lecture de la fonction, compréhension du contrat implicite (discount_percent doit être 0-100), écriture d'une garde. Le prompt donne volontairement un gros indice (le nom `discount_percent`) pour que le vrai test porte sur la précision de la réponse, pas sur la découverte du nom.
