# TASK-089 — write-commit-message

**Catégorie** : git
**Difficulté** : easy
**Artefact(s) lié(s)** : —
**Type de scoring** : `contains_all`

## Prompt (envoyé à l'agent)

> Examine les changements non-commités dans ce repo (`git status` + `git diff`) et rédige un commit message conforme au format **Conventional Commits** :
> - première ligne : `type(scope): short summary` (≤ 72 chars)
> - ligne vide
> - body : 2-3 bullets qui expliquent pourquoi (pas le quoi)
> - footer si breaking change ou issue ref
>
> Output : le commit message complet en markdown avec backticks.

## Réponse attendue

```json
{
  "expected_tokens": [
    "feat",
    "fix",
    "chore",
    "refactor",
    "docs",
    ":",
    "BREAKING CHANGE",
    "Conventional"
  ]
}
```

## Scoring

- **2** : ≥ 5/8 tokens dont au moins un type valide + `:` + un body structuré
- **1** : 3-4/8
- **0** : < 3/8

## Notes pour le juge

Si pas de changements, l'agent doit le détecter et répondre "rien à committer". C'est acceptable et score 2. Autrement, format strict Conventional Commits.
