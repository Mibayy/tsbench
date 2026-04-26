# TASK-040 — config-consistency

**Catégorie** : cross-language
**Difficulté** : hard
**Artefact(s) lié(s)** : —
**Type de scoring** : `boolean_with_evidence`

## Prompt (envoyé à l'agent)

> Les champs déclarés dans `config/app.config.yaml` (app.name, features.billing, pagination.default, etc.) sont-ils tous effectivement consommés quelque part dans le code ?

## Réponse attendue

```json
{
  "config_file": "config/app.config.yaml",
  "expected_answer": "Aucun champ du YAML n'est effectivement lu par le code généré — le fichier existe mais n'est parsé nulle part.",
  "note": "tâche piège : le fichier YAML est un leurre, seules les env vars sont lues"
}
```

## Scoring

- **2** : oui/non correct ET citation des fichiers/symboles en preuve
- **1** : oui/non correct sans preuve concrète
- **0** : réponse incorrecte

## Notes pour le juge

Hallucination test : un agent qui invente un loader YAML = 0.
