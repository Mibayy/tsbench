# TASK-020 — move-module

**Catégorie** : edit
**Difficulté** : hard
**Artefact(s) lié(s)** : DUP-002
**Type de scoring** : `edit_quality`

## Prompt (envoyé à l'agent)

> La fonction `slugify` dans `apps/api/utils/strings.py` devrait logiquement vivre dans `packages/utils/` pour pouvoir être réutilisée. Déplace-la là-bas et corrige tous les imports.

## Réponse attendue

```json
{
  "from_file": "apps/api/utils/strings.py",
  "to_file": "packages/utils/strings.py",
  "symbol": "slugify"
}
```

## Scoring

- **2** : diff applicable, build/typecheck propre, tous les call sites mis à jour
- **1** : diff applicable mais un call site oublié ou un import cassé
- **0** : diff incorrect, ne compile pas, ou effet de bord non demandé

## Notes pour le juge

Lié à DUP-002 : il existe déjà un `to_slug` dupliqué dans packages/utils/slug_copy.py — l'agent peut optionnellement le consolider.
