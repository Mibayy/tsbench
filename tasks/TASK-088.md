# TASK-088 — document-edge-cases

**Catégorie** : documentation
**Difficulté** : medium
**Artefact(s) lié(s)** : —
**Type de scoring** : `llm_judge`

## Prompt (envoyé à l'agent)

> Pour la fonction `calculate_invoice(payload: dict, user_id: int = 0)` de `apps/api/services/billing.py`, produis une section "Edge Cases" en markdown qui documente :
> - les valeurs de payload qui produisent un comportement inattendu
> - les dépendances externes qui peuvent casser la fonction (DB, config, logging)
> - les hypothèses implicites (ex: user_id > 0)
> - les interactions avec des concurrent calls (idempotence, race)
> - le comportement sur payload vide {}

## Réponse attendue

```json
{
  "rubric": {
    "score_2_criteria": [
      "Liste ≥ 4 edge cases distincts",
      "Au moins 1 edge case sur les deps externes (DB/config/mailer)",
      "Mentionne explicitement l'hypothèse user_id positif (ou équivalent)",
      "Ton neutre/factuel, pas d'invention de fonctionnalités absentes"
    ],
    "score_1_criteria": ["3 edge cases distincts, partiellement documentés"],
    "score_0_criteria": ["< 3 edge cases ou invente des comportements"]
  }
}
```

## Scoring

- **2** : 4/4 critères
- **1** : 2-3/4
- **0** : 0-1/4

## Notes pour le juge

Test de raisonnement défensif sur du code existant. La fonction a volontairement beaucoup de "filler" (x_0..x_17) pour que l'agent doive distinguer le vrai comportement.
