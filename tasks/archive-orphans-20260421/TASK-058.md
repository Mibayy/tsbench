# TASK-058 -- performance-hotspots

**Categorie** : audit
**Difficulte** : medium
**Artefact(s) lie(s)** : HOTSPOT-001, HOTSPOT-002, HOTSPOT-003, HOTSPOT-004, HOTSPOT-005
**Type de scoring** : `contains_all`

## Prompt (envoye a l'agent)

> Identifie les 5 fonctions les plus complexes dans le repertoire `apps/` du projet (par complexite cyclomatique, branches, nesting). Ignore bench.py et generate.py. Classe-les par ordre decroissant.

## Réponse attendue

```json
{
  "must_contain": [
    "orchestrate_nightly_job",
    "reconcile_payments",
    "route_webhook_event",
    "authenticate_multi_factor",
    "validate_contract"
  ]
}
```

## Scoring

- **2** : >=4 des 5 hotspots identifies (orchestrate_nightly_job CC=15, reconcile_payments CC=14, route_webhook_event CC=14, authenticate_multi_factor CC=13, validate_contract CC=12)
- **1** : 2-3 hotspots identifies
- **0** : <2

## Notes pour le juge

Teste `find_hotspots`. Les 5 hotspots reels sont plantes avec des complexites cyclomatiques connues.
