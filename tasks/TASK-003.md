# TASK-003 — find-env-usage

**Catégorie** : localisation
**Difficulté** : easy
**Artefact(s) lié(s)** : UNDECL-001
**Type de scoring** : `exact_match`

## Prompt (envoyé à l'agent)

> Où est utilisée la variable d'environnement `SECRET_UNDECLARED_TOKEN` dans le code ? Donne-moi le fichier et la fonction.

## Réponse attendue

```json
{
  "env_var": "SECRET_UNDECLARED_TOKEN",
  "file": "apps/api/utils/secret_reader.py",
  "function": "get_secret_config"
}
```

## Scoring

- **2** : fichier + symbole + ligne (±3) corrects
- **1** : fichier + symbole corrects, ligne hors tolérance
- **0** : symbole incorrect ou non trouvé

## Notes pour le juge

Cette variable est lue mais pas déclarée dans .env.example (UNDECL). Une seule référence dans le code.
