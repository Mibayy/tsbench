# TASK-092 — verbose-bash-top-ips

**Catégorie** : data_analysis
**Difficulté** : medium
**Type de scoring** : `set_match_loose`

## Prompt (envoyé à l'agent)

> Dans le fichier `tasks/fixtures/access.log`, quelles sont les **3 IPs les plus actives** (top par nombre de requêtes) ? Renvoie un JSON `{"top_ips": ["1.2.3.4", ...]}` ordonné desc. *(Data files in tasks/fixtures/ are NOT code files. Use `Bash` to read/grep/awk them — this is NOT a code-navigation task.)*

## Réponse attendue

```json
{
  "top_ips": [
    "10.0.5.27",
    "10.0.1.130",
    "10.0.2.148"
  ]
}
```

## Scoring

- **2** : 3 IPs correctes, ordre exact
- **1** : 2-3 IPs correctes, ordre approximatif
- **0** : ≤1 IP correcte

## Notes pour le juge

Idem TASK-091 sur le log de 75 KB, mais agrégation différente. L'agent peut combiner `awk '{print $1}' | sort | uniq -c | sort -rn | head`. Le résultat brut de `awk` sur 700 lignes fait 12 KB, juste au-dessus du seuil capture.
