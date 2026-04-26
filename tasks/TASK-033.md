# TASK-033 — diff-summary

**Catégorie** : review
**Difficulté** : medium
**Artefact(s) lié(s)** : BREAK-001, BREAK-002, BREAK-003, BREAK-004, BREAK-005, BREAK-006
**Type de scoring** : `set_match_strict`

## Prompt (envoyé à l'agent)

> Résume symbole par symbole tous les changements entre le tag `v1` et le tag `v2`. Je veux une bullet list courte.

## Réponse attendue

```json
{
  "expected_changes": [
    {
      "id": "BREAK-001",
      "kind": "rename_function",
      "from": "compute_invoice",
      "to": "calculate_invoice"
    },
    {
      "id": "BREAK-002",
      "kind": "signature_change",
      "symbol": "authenticate_user"
    },
    {
      "id": "BREAK-003",
      "kind": "remove_function",
      "symbol": "bulk_import_members"
    },
    {
      "id": "BREAK-004",
      "kind": "type_change",
      "symbol": "MembersStatus"
    },
    {
      "id": "BREAK-005",
      "kind": "route_removed",
      "route": "DELETE /api/webhooks/{id}"
    },
    {
      "id": "BREAK-006",
      "kind": "default_change",
      "symbol": "DEFAULT_PAGE_SIZE"
    }
  ],
  "expected_count": 6
}
```

## Scoring

- **2** : liste exactement égale à la liste attendue (F1 = 1.0)
- **1** : F1 ≥ 0.75 (un ou deux éléments manquants ou en trop)
- **0** : F1 < 0.75

## Notes pour le juge

6 BREAK-* exactement. Oublier un seul = F1 < 1.
