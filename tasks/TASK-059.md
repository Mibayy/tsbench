# TASK-059 -- git-status

**Categorie** : git
**Difficulte** : easy
**Artefact(s) lie(s)** :
**Type de scoring** : `contains_all`

## Prompt (envoye a l'agent)

> Donne le status git du projet : branche courante, fichiers modifies, fichiers staged, fichiers non-tracked. Utilise l'outil dedie au git status.

## Réponse attendue

```json
{
  "must_contain": [
    "branch"
  ]
}
```

## Scoring

- **2** : branche + status complet (staged, unstaged, untracked)
- **1** : branche identifiee mais status partiel
- **0** : echec

## Notes pour le juge

Teste `get_git_status`. Equivalent structure de `git status` avec parsing JSON.
