# TASK-003 — find-schema-field

**Catégorie** : localisation
**Difficulté** : easy
**Artefact(s) lié(s)** : —
**Type de scoring** : `exact_match`

## Prompt (envoyé à l'agent)

> Dans quelle table et quelle colonne est stocké le rôle d'un membre d'association ? Donne le fichier de schéma.

## Réponse attendue

```json
{
  "file": "packages/db/schema.prisma",
  "table": "Member",
  "column": "role"
}
```

## Scoring

- **2** : fichier + symbole + ligne (±3) corrects
- **1** : fichier + symbole corrects, ligne hors tolérance
- **0** : symbole incorrect ou non trouvé

## Notes pour le juge

Schéma Prisma unique : packages/db/schema.prisma, model Member, champ role String.
