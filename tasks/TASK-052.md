# TASK-052 — code-gen-password-hasher

**Catégorie** : code_generation
**Difficulté** : medium
**Artefact(s) lié(s)** : —
**Type de scoring** : `contains_all`

## Prompt (envoyé à l'agent)

> Implémente `hash_password(password: str) -> str` et `verify_password(password: str, hashed: str) -> bool` dans `packages/utils/password.py`. Utilise **PBKDF2-SHA256** via `hashlib.pbkdf2_hmac` avec 200000 iterations minimum, un salt aléatoire de 16 octets, encodage final `iterations$salt_hex$hash_hex`. `verify_password` utilise `hmac.compare_digest` pour constant-time.

## Réponse attendue

```json
{
  "expected_tokens": [
    "def hash_password",
    "def verify_password",
    "pbkdf2_hmac",
    "os.urandom",
    "compare_digest",
    "200000",
    "hexdigest",
    "packages/utils/password.py"
  ]
}
```

## Scoring

- **2** : ≥ 7/8 tokens
- **1** : 4-6/8
- **0** : < 4/8

## Notes pour le juge

Points critiques : salt aléatoire (pas fixe), constant-time compare (pas `==`), iterations ≥ 100k. Une solution naïve sha256(password) scorerait 0.
