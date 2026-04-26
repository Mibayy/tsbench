# TASK-011 — rename-symbol

**Catégorie** : edit
**Difficulté** : hard
**Artefact(s) lié(s)** : AMBIG-001
**Type de scoring** : `edit_quality`

## Prompt (envoyé à l'agent)

> Renomme la fonction `create_user` définie dans `apps/api/ambig/mod1.py` en `create_regular_user`, en mettant à jour tous ses call sites. Attention : une autre fonction du même nom existe dans `apps/api/ambig/mod2.py` — elle ne doit PAS être touchée.

## Réponse attendue

```json
{
  "target_file": "apps/api/ambig/mod1.py",
  "before_symbol": "create_user",
  "after_symbol": "create_regular_user",
  "must_not_touch": "apps/api/ambig/mod2.py"
}
```

## Scoring

- **2** : diff applicable, build/typecheck propre, tous les call sites mis à jour
- **1** : diff applicable mais un call site oublié ou un import cassé
- **0** : diff incorrect, ne compile pas, ou effet de bord non demandé

## Notes pour le juge

Test de précision sur symbole ambigu. Renommer mod2 est une erreur éliminatoire.
