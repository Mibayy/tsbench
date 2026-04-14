# TASK-006 — find-component-usage

**Catégorie** : localisation
**Difficulté** : medium
**Artefact(s) lié(s)** : —
**Type de scoring** : `set_match_loose`

## Prompt (envoyé à l'agent)

> Quels fichiers importent et utilisent le composant React `<Sidebar>` ?

## Réponse attendue

```json
{
  "component": "Sidebar",
  "imported_in_pattern": "apps/web/app/*/page.tsx",
  "min_expected_count": 15
}
```

## Scoring

- **2** : la réponse contient au moins N éléments corrects parmi ceux attendus
- **1** : au moins la moitié des éléments attendus sont cités
- **0** : aucun élément correct

## Notes pour le juge

Toutes les pages app/*/page.tsx importent Sidebar. ~15 pages + home.
