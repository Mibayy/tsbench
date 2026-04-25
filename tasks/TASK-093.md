# TASK-093 — large-json-extract

**Catégorie** : data_analysis
**Difficulté** : easy
**Type de scoring** : `exact_match`

## Prompt (envoyé à l'agent)

> Dans le fichier `tasks/fixtures/services.json` (config services, 21 KB), quelle est la valeur de `services["svc-027"].mem_limit_mb` ? Renvoie un JSON `{"mem_limit_mb": <int>}`. *(Data files in tasks/fixtures/ are NOT code files. Use `Bash` to read/grep/awk them — this is NOT a code-navigation task.)*

## Réponse attendue

```json
{
  "mem_limit_mb": 2048
}
```

## Scoring

- **2** : valeur exacte (2048)
- **0** : valeur incorrecte ou absente

## Notes pour le juge

L'agent peut soit `cat services.json | jq '.services["svc-027"].mem_limit_mb'`, soit lire le fichier en entier puis parser. Sans tool_capture, charger 21 KB de JSON dans le contexte coûte directement. Avec, l'output Bash est sandbox et l'agent fait `capture_aggregate(transform="extract:\"mem_limit_mb\":\\s*\\d+")` ou utilise jq direct.
