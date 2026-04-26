# TASK-042 — code-gen-slugify

**Catégorie** : code_generation
**Difficulté** : medium
**Artefact(s) lié(s)** : —
**Type de scoring** : `contains_all`

## Prompt (envoyé à l'agent)

> Dans `packages/utils/`, écris une nouvelle fonction `slugify(text: str) -> str` qui transforme une string en slug URL-safe selon ces règles :
> - lowercase
> - espaces et underscores → un seul tiret `-`
> - retire les accents (é→e, ü→u, ç→c) — utilise `unicodedata.normalize('NFKD', ...)` + filtrage ASCII
> - retire tout caractère non alphanumérique (sauf tirets)
> - strip les tirets en début/fin
> - collapse les tirets consécutifs
>
> Donne-moi le code complet de la fonction (avec les imports nécessaires) et indique le fichier où tu la mettrais.

## Réponse attendue

```json
{
  "expected_tokens": [
    "def slugify",
    "text: str",
    "-> str",
    "unicodedata",
    "normalize",
    "NFKD",
    "lower",
    "packages/utils"
  ]
}
```

## Scoring

- **2** : ratio de tokens présents ≥ 0.9 (7/8 ou 8/8)
- **1** : ratio ≥ 0.5 (4/8)
- **0** : ratio < 0.5

## Notes pour le juge

Teste la capacité à écrire du code propre depuis un spec. `contains_all` vérifie présence des éléments structurels clés (signature, normalisation Unicode, localisation fichier). Tolère les différences mineures de style mais pénalise les solutions qui ratent la partie accents (NFKD).
