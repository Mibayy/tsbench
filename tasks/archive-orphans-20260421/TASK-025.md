# TASK-025 — hotspot-audit

**Catégorie** : audit
**Difficulté** : medium
**Artefact(s) lié(s)** : HOTSPOT-001, HOTSPOT-002, HOTSPOT-003, HOTSPOT-004, HOTSPOT-005
**Type de scoring** : `set_match_strict`

## Prompt (envoyé à l'agent)

> Trouve les 3 fonctions les plus complexes (plus haute complexite cyclomatique) dans le code applicatif du projet (apps/ et packages/). Ignore bench.py et generate.py.

## Réponse attendue

```json
{
  "top3_expected": [
    {
      "symbol": "orchestrate_nightly_job",
      "cyclomatic": 15,
      "file": "apps/worker/tasks/complex_pipeline.py"
    },
    {
      "symbol": "reconcile_payments",
      "cyclomatic": 14,
      "file": "apps/api/services/complex_billing.py"
    },
    {
      "symbol": "route_webhook_event",
      "cyclomatic": 14,
      "file": "apps/api/services/complex_routing.py"
    }
  ]
}
```

## Scoring

- **2** : liste exactement égale à la liste attendue (F1 = 1.0)
- **1** : F1 ≥ 0.75 (un ou deux éléments manquants ou en trop)
- **0** : F1 < 0.75

## Notes pour le juge

Top 3 attendu : orchestrate_nightly_job, reconcile_payments, route_webhook_event (complexités 15, 14, 14).
