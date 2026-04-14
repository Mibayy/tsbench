# TASK-019 — extract-constant

**Catégorie** : edit
**Difficulté** : medium
**Artefact(s) lié(s)** : BREAK-006
**Type de scoring** : `edit_quality`

## Prompt (envoyé à l'agent)

> Plusieurs modules utilisent le nombre magique `20` comme taille de page par défaut. Extrais-le dans une constante `DEFAULT_PAGE_SIZE` centralisée et mets à jour tous les usages.

## Réponse attendue

```json
{
  "magic_number": 20,
  "constant_name": "DEFAULT_PAGE_SIZE",
  "min_files_touched": 2
}
```

## Scoring

- **2** : diff applicable, build/typecheck propre, tous les call sites mis à jour
- **1** : diff applicable mais un call site oublié ou un import cassé
- **0** : diff incorrect, ne compile pas, ou effet de bord non demandé

## Notes pour le juge

Concerne apps/api/config.py et apps/api/utils/pagination.py au minimum.
