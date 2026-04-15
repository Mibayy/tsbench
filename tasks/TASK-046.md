# TASK-046 — billing-hotspots

**Catégorie** : heavy_read
**Difficulté** : hard
**Artefact(s) lié(s)** :
**Type de scoring** : `contains_all`

## Prompt (envoyé à l'agent)

> Donne-moi le source complet des 3 fonctions les plus longues (en nombre de lignes) dans `apps/api/services/billing.py`. Pour chacune : nom, nombre de lignes, et le code entier.

## Réponse attendue

```json
{
  "must_contain": [
    "def",
    "billing",
    "payload"
  ]
}
```

## Scoring

- **2** : 3 fonctions nommées avec source complet visible
- **1** : 1 ou 2 fonctions avec source
- **0** : pas de source ou seulement des signatures

## Notes pour le juge

Le fichier fait 648 lignes et contient ~30 fonctions. Baseline : Read du fichier entier + comptage manuel. TS : `find_hotspots` ou `get_function_source` ciblé.
