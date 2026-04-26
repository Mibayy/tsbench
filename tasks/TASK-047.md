# TASK-047 — code-gen-jwt-signer

**Catégorie** : code_generation
**Difficulté** : hard
**Artefact(s) lié(s)** : —
**Type de scoring** : `contains_all`

## Prompt (envoyé à l'agent)

> Implémente une mini fonction `sign_jwt(payload: dict, secret: str, exp_seconds: int = 3600) -> str` dans `packages/utils/jwt_sign.py`. Elle doit produire un JWT HS256 conforme **sans utiliser de lib PyJWT** — uniquement `hmac`, `hashlib`, `base64`, `json`, `time`. Format attendu : `<header_b64>.<payload_b64>.<sig_b64>` où les 3 segments sont du **base64url sans padding**. Le payload injecté doit contenir `exp = int(time.time()) + exp_seconds`.

## Réponse attendue

```json
{
  "expected_tokens": [
    "import hmac",
    "import hashlib",
    "sha256",
    "base64.urlsafe_b64encode",
    "rstrip",
    "exp",
    "time.time()",
    "HS256",
    "packages/utils/jwt_sign.py"
  ]
}
```

## Scoring

- **2** : ≥ 7/9 tokens (HMAC + base64url sans padding + exp calculé)
- **1** : 4-6/9
- **0** : < 4/9

## Notes pour le juge

Piège classique : utiliser `base64.b64encode` (standard) au lieu de `urlsafe_b64encode`, ou oublier le `rstrip(b'=')` pour supprimer le padding.
