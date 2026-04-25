# TASK-091 — verbose-bash-top-endpoints

**Catégorie** : data_analysis
**Difficulté** : medium
**Type de scoring** : `set_match_loose`

## Prompt (envoyé à l'agent)

> Dans le fichier `tasks/fixtures/access.log` (nginx access log, 75 KB), quels sont les **5 endpoints les plus appelés** ? Renvoie un JSON `{"top_endpoints": ["/path1", ...]}` ordonné par fréquence décroissante. *(Data files in tasks/fixtures/ are NOT code files. Use `Bash` to read/grep/awk them — this is NOT a code-navigation task.)*

## Réponse attendue

```json
{
  "top_endpoints": [
    "/api/products",
    "/api/cart",
    "/api/checkout",
    "/api/users",
    "/healthz"
  ]
}
```

## Scoring

- **2** : les 5 bons endpoints, ordre exact
- **1** : 4-5 bons endpoints, ordre incorrect
- **0** : ≤3 endpoints corrects

## Notes pour le juge

L'agent doit lire un fichier de 75 KB. Sans `tool_capture`, le contenu inonde le contexte. Avec, l'output Bash est sandbox et l'agent peut lancer des commandes structurées (`grep -oE` + `sort | uniq -c | sort -rn | head -5`) puis utiliser `capture_aggregate` ou `capture_search` pour récupérer les compteurs.
