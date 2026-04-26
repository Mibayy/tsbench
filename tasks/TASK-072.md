# TASK-072 — refactor-dedupe-similar

**Catégorie** : refactoring
**Difficulté** : medium
**Artefact(s) lié(s)** : —
**Type de scoring** : `contains_all`

## Prompt (envoyé à l'agent)

> Ces 3 fonctions répètent la même structure :
>
> ```python
> def export_users_csv(users): ...  # 25 lignes : open file, csv.writer, iter rows, close
> def export_orders_csv(orders): ...  # idem, 25 lignes
> def export_invoices_csv(invoices): ...  # idem, 25 lignes
> ```
>
> Propose un refactor. Extrais la logique commune dans `_export_to_csv(rows: Iterable, columns: list[str], path: str)` et fais des trois fonctions des wrappers courts qui préparent les colonnes. Donne pseudo-code des 3 wrappers + du helper.

## Réponse attendue

```json
{
  "expected_tokens": [
    "def _export_to_csv",
    "Iterable",
    "columns",
    "path",
    "csv.writer",
    "writerow",
    "wrapper",
    "DRY"
  ]
}
```

## Scoring

- **2** : ≥ 6/8 tokens (helper extrait + wrappers minces + DRY invoqué)
- **1** : 3-5/8
- **0** : < 3/8

## Notes pour le juge

Le helper prend en paramètre les colonnes ET le path. Les 3 wrappers se résument à préparer les rows+columns et appeler le helper. Piège : laisser trop de logique dans les wrappers = refactor raté.
