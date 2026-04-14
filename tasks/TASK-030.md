# TASK-030 — dockerfile-audit

**Catégorie** : infra
**Difficulté** : easy
**Artefact(s) lié(s)** : DOCKER-001, DOCKER-002
**Type de scoring** : `set_match_strict`

## Prompt (envoyé à l'agent)

> Review les Dockerfiles dans `infra/docker/`. Quels sont les problèmes que tu vois ?

## Réponse attendue

```json
{
  "expected_issues": [
    {
      "id": "DOCKER-001",
      "file": "infra/docker/worker.Dockerfile",
      "issue": "uses python:latest base image"
    },
    {
      "id": "DOCKER-002",
      "file": "infra/docker/web.Dockerfile",
      "issue": "exposes unused ports 9229 and 6666"
    }
  ],
  "count": 2
}
```

## Scoring

- **2** : liste exactement égale à la liste attendue (F1 = 1.0)
- **1** : F1 ≥ 0.75 (un ou deux éléments manquants ou en trop)
- **0** : F1 < 0.75

## Notes pour le juge

3 Dockerfiles : api (propre), worker (latest tag), web (ports debug exposés).
