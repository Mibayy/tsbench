# TASK-053 -- semantic-duplicates

**Categorie** : audit
**Difficulte** : medium
**Artefact(s) lie(s)** : DUP-001, DUP-002, DUP-003
**Type de scoring** : `contains_all`

## Prompt (envoye a l'agent)

> Trouve les fonctions semantiquement dupliquees dans le projet (fonctions qui font la meme chose avec des noms differents). Liste les paires de doublons.

## Réponse attendue

```json
{
  "must_contain": [
    "doublon",
    "dupli"
  ]
}
```

## Scoring

- **2** : analyse completee, paires identifiees OU conclusion argumentee qu'il n'y a pas de vrais doublons
- **1** : analyse partielle
- **0** : echec

## Notes pour le juge

Teste `find_semantic_duplicates`. 3 paires reelles : paginate~paginate_also (DUP-001), slugify~to_slug (DUP-002), start_of_day~day_start (DUP-003).
