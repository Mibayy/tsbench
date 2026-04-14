# TASK-029 — secret-detection

**Catégorie** : config
**Difficulté** : medium
**Artefact(s) lié(s)** : SECRET-001, SECRET-002, SECRET-003
**Type de scoring** : `set_match_strict`

## Prompt (envoyé à l'agent)

> Y a-t-il des secrets (clés API, tokens, credentials) exposés dans les fichiers du dossier `config/` ?

## Réponse attendue

```json
{
  "expected_secrets": [
    "STRIPE_API_KEY",
    "STRIPE_WEBHOOK_SECRET",
    "AWS_SECRET_ACCESS_KEY"
  ],
  "file": "config/.env.staging",
  "count": 3
}
```

## Scoring

- **2** : liste exactement égale à la liste attendue (F1 = 1.0)
- **1** : F1 ≥ 0.75 (un ou deux éléments manquants ou en trop)
- **0** : F1 < 0.75

## Notes pour le juge

3 secrets plantés dans .env.staging (valeurs obfusquées en placeholders pour GitHub push protection — la détection se fait par nom de variable).
