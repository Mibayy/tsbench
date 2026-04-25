# TASK-094 — count-todos-corpus

**Catégorie** : data_analysis
**Difficulté** : easy
**Type de scoring** : `exact_match`

## Prompt (envoyé à l'agent)

> Dans `tasks/fixtures/codebase_dump.txt` (44 KB de code dumpé multi-fichiers), combien y a-t-il de commentaires `# TODO` exactement ? Et combien de `# FIXME` ? Renvoie un JSON `{"todo": <int>, "fixme": <int>}`. *(Data files in tasks/fixtures/ are NOT code files. Use `Bash` to read/grep/awk them — this is NOT a code-navigation task.)*

## Réponse attendue

```json
{
  "todo": 132,
  "fixme": 64
}
```

## Scoring

- **2** : todo=132 ET fixme=64
- **1** : un des deux correct
- **0** : aucun correct

## Notes pour le juge

Comptage simple via `grep -c '# TODO' fixture` et `grep -c '# FIXME' fixture`. Si l'agent fait `cat | head` ou similaire le contexte gonfle, mais avec `grep -c` (count-only) il évite tout dump et `tool_capture` n'a presque rien à faire — c'est le **path optimal** que le SYSTEM_PROMPT_TS et la présence de `capture_aggregate(transform="count:...")` doivent encourager.
