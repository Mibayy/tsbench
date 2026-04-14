# TASK-027 — orphan-env

**Catégorie** : config
**Difficulté** : easy
**Artefact(s) lié(s)** : ORPHAN-001, ORPHAN-002, ORPHAN-003, ORPHAN-004
**Type de scoring** : `set_match_strict`

## Prompt (envoyé à l'agent)

> Liste les variables d'environnement déclarées dans les fichiers `.env.example` mais qui ne sont jamais lues dans le code.

## Réponse attendue

```json
{
  "expected_orphans": [
    "LEGACY_SMTP_HOST",
    "LEGACY_SMTP_PORT",
    "UNUSED_FEATURE_FLAG",
    "OLD_ANALYTICS_TOKEN"
  ],
  "count": 4
}
```

## Scoring

- **2** : liste exactement égale à la liste attendue (F1 = 1.0)
- **1** : F1 ≥ 0.75 (un ou deux éléments manquants ou en trop)
- **0** : F1 < 0.75

## Notes pour le juge

4 orphans plantés : LEGACY_SMTP_HOST, LEGACY_SMTP_PORT, UNUSED_FEATURE_FLAG, OLD_ANALYTICS_TOKEN
