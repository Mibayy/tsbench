# TASK-051 — code-gen-webhook-sender

**Catégorie** : code_generation
**Difficulté** : medium
**Artefact(s) lié(s)** : —
**Type de scoring** : `contains_all`

## Prompt (envoyé à l'agent)

> Implémente `send_webhook(url: str, payload: dict, *, secret: str, timeout: float = 5.0) -> dict` dans `packages/utils/webhook.py`. Utilise `requests` (import en haut). Le payload JSON doit être signé HMAC-SHA256 avec `secret`, signature envoyée dans header `X-Signature: sha256=<hex>`. Retourne `{"status": int, "body": str, "error": str | None}`. Capture les `requests.RequestException` → retourne status=0, error=str(e).

## Réponse attendue

```json
{
  "expected_tokens": [
    "import requests",
    "def send_webhook",
    "hmac.new",
    "hexdigest",
    "X-Signature",
    "sha256=",
    "timeout",
    "RequestException",
    "packages/utils/webhook.py"
  ]
}
```

## Scoring

- **2** : ≥ 7/9 tokens
- **1** : 4-6/9
- **0** : < 4/9

## Notes pour le juge

Signature = `hmac.new(secret.encode(), json_body, hashlib.sha256).hexdigest()`. Piège : ne pas signer le body sérialisé tel qu'envoyé.
