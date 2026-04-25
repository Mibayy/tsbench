# TASK-095 — npm-build-error-extract

**Catégorie** : data_analysis
**Difficulté** : medium
**Type de scoring** : `judge_match`

## Prompt (envoyé à l'agent)

> Dans `tasks/fixtures/npm-install.log` (24 KB de output `npm install` verbose), quel est le **module manquant** qui cause l'erreur ? Renvoie un JSON `{"missing_module": "<name>"}`. *(Data files in tasks/fixtures/ are NOT code files. Use `Bash` to read/grep/awk them — this is NOT a code-navigation task.)*

## Réponse attendue

```json
{
  "missing_module": "@scope/missing-pkg"
}
```

## Scoring

- **2** : `@scope/missing-pkg` exact
- **1** : substring `missing-pkg` reconnu
- **0** : autre

## Notes pour le juge

La ligne `npm ERR! Cannot find module '@scope/missing-pkg'` est noyée dans 280 lignes de fetch logs. L'agent doit `grep "Cannot find" log` ou `tail` puis filtrer. Output potentiellement >4 KB → tool_capture sandbox → agent extrait le module via `capture_aggregate(transform="extract:'@[^']+'")`.
