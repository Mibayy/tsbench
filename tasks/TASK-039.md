# TASK-039 — ts-py-type-mapping

**Catégorie** : cross-language
**Difficulté** : hard
**Artefact(s) lié(s)** : —
**Type de scoring** : `exact_match`

## Prompt (envoyé à l'agent)

> Le type TypeScript `Members` déclaré dans `packages/shared-types/members.ts` correspond à quel modèle Python dans le backend ? Donne le fichier et le nom de la classe.

## Réponse attendue

```json
{
  "ts_type": "Members",
  "ts_file": "packages/shared-types/members.ts",
  "py_class": "Member",
  "py_file": "apps/api/models/members.py"
}
```

## Scoring

- **2** : fichier + symbole + ligne (±3) corrects
- **1** : fichier + symbole corrects, ligne hors tolérance
- **0** : symbole incorrect ou non trouvé

## Notes pour le juge

Cross-langage : Token Savior ne suit pas les liens cross-langage, la correspondance est par convention de nom.
