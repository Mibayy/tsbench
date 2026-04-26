# TASK-058 — code-gen-cli-parser

**Catégorie** : code_generation
**Difficulté** : medium
**Artefact(s) lié(s)** : —
**Type de scoring** : `contains_all`

## Prompt (envoyé à l'agent)

> Écris un CLI `scripts/cleanup_stale.py` avec `argparse` qui prend :
> - `--dry-run` (flag boolean)
> - `--older-than DAYS` (int, défaut 30)
> - `--path PATH` (str, required, nargs='+' pour plusieurs)
> - sous-command `report` vs `delete`
>
> La fonction `main()` parse les args, imprime un résumé des args parsés et exit(0). Donne le code complet.

## Réponse attendue

```json
{
  "expected_tokens": [
    "import argparse",
    "ArgumentParser",
    "add_subparsers",
    "--dry-run",
    "action=\"store_true\"",
    "--older-than",
    "--path",
    "nargs=\"+\"",
    "required=True",
    "scripts/cleanup_stale.py"
  ]
}
```

## Scoring

- **2** : ≥ 8/10 tokens
- **1** : 5-7/10
- **0** : < 5/10

## Notes pour le juge

Subparsers nécessitent `dest=` ou `required=True` selon la version Python. Piège : oublier `action="store_true"` sur le flag dry-run.
