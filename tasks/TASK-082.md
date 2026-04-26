# TASK-082 — explain-data-flow

**Catégorie** : explanation
**Difficulté** : hard
**Artefact(s) lié(s)** : —
**Type de scoring** : `llm_judge`

## Prompt (envoyé à l'agent)

> Trace le flow complet d'une requête POST `/api/orders` depuis la réception HTTP jusqu'à la persistence DB et l'éventuel émission d'événement async. Structure :
> 1. Point d'entrée (route handler)
> 2. Validation du payload
> 3. Couche service (qu'est-ce qui est appelé, dans quel ordre)
> 4. Couche repository / ORM (quelle requête SQL conceptuellement)
> 5. Side-effects (emails, webhooks, events bus)

## Réponse attendue

```json
{
  "rubric": {
    "score_2_criteria": [
      "Identifie au moins 4 des 5 couches avec nom de fonction/classe précis, OU explicite que l'endpoint n'est pas encore wired et décrit le flow le plus proche disponible (ex: test helper, route candidate) avec citations",
      "Ordre de chaînage correct entre les couches décrites",
      "Mentionne au moins un side-effect concret (email OU webhook OU event) OU note explicitement l'absence avec citation",
      "Cite un fichier:ligne au moins à chaque niveau décrit (test file accepté si pas de vrai endpoint)"
    ],
    "score_1_criteria": ["Couvre 2-3 critères avec moins de précision"],
    "score_0_criteria": ["Vue générique ou invente des couches qui n'existent pas"]
  }
}
```

## Scoring

- **2** : 4/4 critères juge
- **1** : 2-3/4
- **0** : 0-1/4

## Notes pour le juge

Test de traçage multi-fichier. TS devrait briller avec `get_call_chain` + `get_function_source`. Natif devrait faire 4-5 Reads + Greps.
