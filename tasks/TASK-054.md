# TASK-054 — code-gen-queue-consumer

**Catégorie** : code_generation
**Difficulté** : hard
**Artefact(s) lié(s)** : —
**Type de scoring** : `contains_all`

## Prompt (envoyé à l'agent)

> Implémente un worker consumer Redis Streams dans `apps/worker/stream_consumer.py`. Fonction `consume(redis_client, stream: str, group: str, consumer_name: str, handler: callable, *, block_ms: int = 5000)`. Elle doit : créer le consumer group si absent (`XGROUP CREATE` avec `MKSTREAM`), loop sur `XREADGROUP`, appeler `handler(msg_id, data)`, `XACK` en cas de succès, log + pas de XACK en cas d'exception (pour retry via PEL).

## Réponse attendue

```json
{
  "expected_tokens": [
    "def consume",
    "xgroup_create",
    "MKSTREAM",
    "xreadgroup",
    "xack",
    "consumer_name",
    "handler",
    "BusyGroupError",
    "apps/worker/stream_consumer.py"
  ]
}
```

## Scoring

- **2** : ≥ 7/9 tokens
- **1** : 4-6/9
- **0** : < 4/9

## Notes pour le juge

`BusyGroupError` pour ignorer "group already exists". Piège : XACK même en cas d'exception → le message est perdu sans retry.
