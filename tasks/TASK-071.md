# TASK-071 — refactor-split-god-class

**Catégorie** : refactoring
**Difficulté** : hard
**Artefact(s) lié(s)** : —
**Type de scoring** : `contains_all`

## Prompt (envoyé à l'agent)

> La classe `OrderManager` (imagine-la avec 30 méthodes) couvre 3 responsabilités : persistence DB, envoi d'emails, calcul de totaux. Propose un plan de refactor pour la splitter en 3 classes avec responsabilités séparées. Donne :
> - le nom des 3 classes cibles et leur responsabilité
> - la nouvelle signature du constructeur `OrderManager` (devient un orchestrateur)
> - comment les 3 nouveaux services sont injectés (DI via constructeur)
> - exemple de migration d'une méthode existante `send_confirmation_email` vers la nouvelle structure

## Réponse attendue

```json
{
  "expected_tokens": [
    "OrderRepository",
    "EmailService",
    "OrderCalculator",
    "dependency injection",
    "single responsibility",
    "SRP",
    "constructor",
    "orchestrator",
    "send_confirmation_email"
  ]
}
```

## Scoring

- **2** : ≥ 7/9 tokens (3 classes nommées + DI explicite + SRP cité)
- **1** : 4-6/9
- **0** : < 4/9

## Notes pour le juge

Les noms exacts importent moins que la séparation claire (repo / email / calc) et le pattern DI. Refuser les réponses qui proposent juste de "splitter le fichier" sans discussion des dépendances.
