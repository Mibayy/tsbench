# TASK-046 — code-gen-csv-parser

**Catégorie** : code_generation
**Difficulté** : medium
**Artefact(s) lié(s)** : —
**Type de scoring** : `contains_all`

## Prompt (envoyé à l'agent)

> Implémente une fonction `parse_csv(text: str, *, has_header: bool = True) -> list[dict]` dans `packages/utils/csv_parse.py`. Elle doit utiliser le module `csv` stdlib (pas de dépendance externe). Si `has_header=True`, chaque ligne devient un dict avec les clés du header ; sinon chaque ligne est un dict `{'col_0': ..., 'col_1': ...}`. Gère correctement les valeurs quotées et les virgules dans les quotes.

## Réponse attendue

```json
{
  "expected_tokens": [
    "import csv",
    "def parse_csv",
    "has_header",
    "csv.reader",
    "StringIO",
    "list[dict]",
    "packages/utils/csv_parse.py"
  ]
}
```

## Scoring

- **2** : ≥ 6/7 tokens
- **1** : 3-5/7
- **0** : < 3/7

## Notes pour le juge

Usage de `csv.DictReader` valide aussi (au lieu de reader + dict manuel). L'important : pas de split(',') naïf.
