# TASK-012 — add-field

**Catégorie** : edit
**Difficulté** : medium
**Artefact(s) lié(s)** : —
**Type de scoring** : `edit_quality`

## Prompt (envoyé à l'agent)

> Ajoute un champ optionnel `archivedAt: DateTime?` au modèle `Member` dans `packages/db/schema.prisma`, puis propage-le aux types TypeScript correspondants dans `apps/web/types/member.ts`.

## Réponse attendue

```json
{
  "schema_file": "packages/db/schema.prisma",
  "model": "Member",
  "new_field": "archivedAt: DateTime?",
  "ts_file": "apps/web/types/member.ts"
}
```

## Scoring

- **2** : diff applicable, build/typecheck propre, tous les call sites mis à jour
- **1** : diff applicable mais un call site oublié ou un import cassé
- **0** : diff incorrect, ne compile pas, ou effet de bord non demandé

## Notes pour le juge

Édition multi-fichier Python/SQL + TS. Validation : diff propre, type TS inclut archivedAt.
