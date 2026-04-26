# TASK-049 — code-gen-validator-email

**Catégorie** : code_generation
**Difficulté** : easy
**Artefact(s) lié(s)** : —
**Type de scoring** : `contains_all`

## Prompt (envoyé à l'agent)

> Implémente `is_valid_email(email: str) -> bool` dans `packages/utils/validate_email.py`. Validation pragmatique : une seule `@`, local-part ≥ 1 char avec `[a-zA-Z0-9._%+-]`, domain avec au moins un `.` et tld de 2-24 chars alphanum. Utilise `re.fullmatch`. Retourne False pour None ou str vide.

## Réponse attendue

```json
{
  "expected_tokens": [
    "import re",
    "def is_valid_email",
    "re.fullmatch",
    "@",
    "bool",
    "return False",
    "packages/utils/validate_email.py"
  ]
}
```

## Scoring

- **2** : ≥ 6/7 tokens
- **1** : 3-5/7
- **0** : < 3/7

## Notes pour le juge

`re.fullmatch` vs `re.match` (match ne vérifie que le début). Piège : une regex trop permissive qui accepte `a@b` sans TLD.
