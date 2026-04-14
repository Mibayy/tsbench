# TASK-037 — project-overview

**Catégorie** : onboarding
**Difficulté** : easy
**Artefact(s) lié(s)** : —
**Type de scoring** : `free_form_rubric`

## Prompt (envoyé à l'agent)

> En 10 bullet points maximum, explique ce que fait ce projet : quel domaine, quelles couches techniques, quels grands modules.

## Réponse attendue

```json
{
  "required_topics": [
    "SaaS / billing / members / sessions / webhooks",
    "FastAPI backend (apps/api)",
    "Next.js frontend (apps/web)",
    "Python worker (apps/worker)",
    "packages/ monorepo (shared-types, db, utils)",
    "Prisma schema (packages/db/schema.prisma)",
    "Docker + k8s + terraform infra"
  ],
  "max_bullets": 10
}
```

## Scoring

- **2** : couvre tous les points clés demandés, sans invention
- **1** : couvre la majorité des points mais en oublie ou invente un détail secondaire
- **0** : réponse incorrecte, très incomplète, ou hallucinations majeures

## Notes pour le juge

Test d'économie de tokens : un bon agent doit éviter de lire tous les 290 fichiers.
