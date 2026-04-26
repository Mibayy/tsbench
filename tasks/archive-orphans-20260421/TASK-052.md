# TASK-052 -- community-detection

**Categorie** : audit
**Difficulte** : hard
**Artefact(s) lie(s)** :
**Type de scoring** : `contains_all`

## Prompt (envoye a l'agent)

> Identifie les communautes (clusters de symboles fortement lies) dans le projet. Pour chaque communaute, donne les symboles principaux et le theme fonctionnel.

## Réponse attendue

```json
{
  "must_contain": [
    "communaut",
    "symbole"
  ]
}
```

## Scoring

- **2** : communautes identifiees avec symboles et themes
- **1** : communautes listees sans theme clair
- **0** : echec

## Notes pour le juge

Teste `get_community` / `get_components`. Analyse structurelle de haut niveau par clustering du graphe de dependances.
