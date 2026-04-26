# TASK-055 — code-gen-url-signer

**Catégorie** : code_generation
**Difficulté** : hard
**Artefact(s) lié(s)** : —
**Type de scoring** : `contains_all`

## Prompt (envoyé à l'agent)

> Implémente `sign_url(url: str, secret: str, expires_in: int = 3600) -> str` et `verify_signed_url(signed_url: str, secret: str) -> bool` dans `packages/utils/url_signer.py`. La signature = HMAC-SHA256 de `url + exp_timestamp`, ajoutée en query param `?sig=<hex>&exp=<int>`. `verify_signed_url` doit : (1) parser les params, (2) vérifier `exp > now()`, (3) recalculer et comparer la sig avec `hmac.compare_digest`.

## Réponse attendue

```json
{
  "expected_tokens": [
    "def sign_url",
    "def verify_signed_url",
    "urllib.parse",
    "hmac",
    "sha256",
    "compare_digest",
    "exp",
    "sig",
    "packages/utils/url_signer.py"
  ]
}
```

## Scoring

- **2** : ≥ 7/9 tokens
- **1** : 4-6/9
- **0** : < 4/9

## Notes pour le juge

Piège : signer l'URL après avoir ajouté `sig` (récursif) ou comparer les sigs avec `==` (timing attack).
