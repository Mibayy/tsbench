# TASK-034 — pr-risk

**Catégorie** : review
**Difficulté** : hard
**Artefact(s) lié(s)** : BREAK-001, BREAK-002, BREAK-003, BREAK-004, BREAK-005, BREAK-006
**Type de scoring** : `set_match_loose`

## Prompt (envoyé à l'agent)

> Parmi les changements entre v1 et v2, lesquels sont les plus risqués et méritent une review attentive avant merge ? Classe-les par criticité.

## Réponse attendue

```json
{
  "high_risk_expected": [
    "authenticate_user",
    "bulk_import_members",
    "delete_webhooks"
  ],
  "rationale": "signature/remove/route removal = breaking pour consumers externes (BREAK-002 authenticate_user signature, BREAK-003 bulk_import_members removed, BREAK-005 DELETE /api/webhooks route removed)"
}
```

## Scoring

- **2** : la réponse contient au moins N éléments corrects parmi ceux attendus
- **1** : au moins la moitié des éléments attendus sont cités
- **0** : aucun élément correct

## Notes pour le juge

Subjectif mais BREAK-002/003/005 sont objectivement les plus cassants (API contract).
