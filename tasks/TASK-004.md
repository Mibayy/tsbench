# TASK-004 — find-route

**Catégorie** : localisation
**Difficulté** : easy
**Artefact(s) lié(s)** : —
**Type de scoring** : `exact_match`

## Prompt (envoyé à l'agent)

> Quel fichier handle la route `POST /api/billing` dans le backend ?

## Réponse attendue

```json
{
  "file": "apps/api/routers/billing.py",
  "handler": "create_billing",
  "method": "POST",
  "path": "/api/billing"
}
```

## Scoring

- **2** : fichier + symbole + ligne (±3) corrects
- **1** : fichier + symbole corrects, ligne hors tolérance
- **0** : symbole incorrect ou non trouvé

## Notes pour le juge

Routes définies dans routers/billing.py via ROUTES.append tuples. Handler 'create_billing'.
