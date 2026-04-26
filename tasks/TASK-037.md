# TASK-037 — undecl-env

**Catégorie** : config
**Difficulté** : medium
**Artefact(s) lié(s)** : UNDECL-001, UNDECL-002
**Type de scoring** : `set_match_strict`

## Prompt (envoyé à l'agent)

> Liste les variables d'environnement lues dans le code Python mais absentes de `config/.env.example`.

## Réponse attendue

```json
{
  "expected_undeclared": [
    "SECRET_UNDECLARED_TOKEN",
    "TSBENCH_HIDDEN_REGION"
  ],
  "count": 2
}
```

## Scoring

- **2** : liste exactement égale à la liste attendue (F1 = 1.0)
- **1** : F1 ≥ 0.75 (un ou deux éléments manquants ou en trop)
- **0** : F1 < 0.75

## Notes pour le juge

2 undeclared plantées : SECRET_UNDECLARED_TOKEN, TSBENCH_HIDDEN_REGION (dans apps/api/utils/secret_reader.py).
