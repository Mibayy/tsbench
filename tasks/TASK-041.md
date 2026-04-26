# TASK-041 -- changed-symbols-since-ref

**Categorie** : git
**Difficulte** : medium
**Artefact(s) lie(s)** :
**Type de scoring** : `contains_all`

## Prompt (envoye a l'agent)

> Quels symboles ont change depuis le commit initial du projet (HEAD~1 ou le premier commit) ? Donne un resume par symbole des changements (ajouts, modifications, suppressions).

## Réponse attendue

```json
{
  "must_contain": [
    "modifi",
    "fonction"
  ]
}
```

## Scoring

- **2** : liste de symboles changes avec type de changement (added/modified/removed)
- **1** : quelques symboles mentionnes sans classification
- **0** : echec

## Notes pour le juge

Teste `get_changed_symbols` ou `get_changed_symbols_since_ref`. Resume symbol-level des changements git.
