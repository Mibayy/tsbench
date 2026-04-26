# TASK-057 -- impacted-tests

**Categorie** : testing
**Difficulte** : medium
**Artefact(s) lie(s)** : HEAVY-READ-045
**Type de scoring** : `set_match_loose`

## Prompt (envoye a l'agent)

> Quels fichiers de tests seraient impactes si on modifie la fonction `authenticate_user` dans `apps/api/services/auth.py` ? Liste les fichiers de test concernes.

## Réponse attendue

```json
{
  "items": [
    "tests/test_auth.py"
  ]
}
```

## Scoring

- **2** : test_auth.py identifie
- **1** : fichier de test lie a auth mentionne
- **0** : aucun

## Notes pour le juge

Teste `find_impacted_test_files`. D'apres HEAVY-READ-045, `apps/api/routers/auth.py` et `tests/test_auth.py` importent le service auth.
