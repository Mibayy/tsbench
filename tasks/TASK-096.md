# TASK-096 — sql-dump-top-country

**Catégorie** : data_analysis
**Difficulté** : medium
**Type de scoring** : `exact_match`

## Prompt (envoyé à l'agent)

> Dans le fichier `tasks/fixtures/users-dump.sql` (60 KB de INSERTs sur la table users), quel est le code pays (champ `country`) qui apparaît le plus de fois ? Renvoie un JSON `{"top_country": "<2-letter-code>"}`. *(Data files in tasks/fixtures/ are NOT code files. Use `Bash` to read/grep/awk them — this is NOT a code-navigation task.)*

## Réponse attendue

```json
{
  "top_country": "BR"
}
```

## Scoring

- **2** : "BR" exact
- **0** : autre code

## Notes pour le juge

Le pays le plus fréquent est BR (87 occurrences). L'agent peut utiliser `grep -oE "'[A-Z]{2}'" file | sort | uniq -c | sort -rn | head -1` ou similaire. L'output brut est 60 KB si lu raw mais après agrégation Bash ~200 octets. Avec `tool_capture`, même un dump intermédiaire est sandbox.
