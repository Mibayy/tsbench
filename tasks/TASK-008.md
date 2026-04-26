# TASK-008 — dead-code-audit

**Catégorie** : audit
**Difficulté** : medium
**Artefact(s) lié(s)** : DEAD-001, DEAD-002, DEAD-003, DEAD-004, DEAD-005, DEAD-006, DEAD-007, DEAD-008, DEAD-009, DEAD-010, DEAD-011, DEAD-012
**Type de scoring** : `set_match_loose`

## Prompt (envoyé à l'agent)

> Donne-moi 5 fonctions exportées qui ne sont jamais appelées nulle part dans le projet.

## Réponse attendue

```json
{
  "min_count_requested": 5,
  "all_dead_symbols": [
    "calculate_legacy_discount",
    "compute_legacy_tax",
    "format_legacy_invoice_id",
    "migrate_v1_session",
    "deprecated_webhook_signer",
    "old_csv_exporter",
    "unused_hash_helper",
    "unused_validator",
    "unused_formatter",
    "legacy_reaper",
    "orphan_cleaner",
    "stale_cache_purger"
  ],
  "scoring": "au moins 5 symboles parmi all_dead_symbols, 0 faux positif"
}
```

## Scoring

- **2** : la réponse contient au moins N éléments corrects parmi ceux attendus
- **1** : au moins la moitié des éléments attendus sont cités
- **0** : aucun élément correct

## Notes pour le juge

12 candidats au total. Liste complète: calculate_legacy_discount, compute_legacy_tax, format_legacy_invoice_id, migrate_v1_session, deprecated_webhook_signer, old_csv_exporter, unused_hash_helper, unused_validator, unused_formatter, legacy_reaper, orphan_cleaner, stale_cache_purger
