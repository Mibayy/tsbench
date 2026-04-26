# TASK-064 — bug-fix-wrong-regex

**Catégorie** : bug_fixing
**Difficulté** : medium
**Artefact(s) lié(s)** : —
**Type de scoring** : `contains_all`

## Prompt (envoyé à l'agent)

> Cette regex doit extraire les numéros de version sémantique `v1.2.3` depuis un texte, mais elle loupe les préversions `v1.2.3-beta.1` :
>
> ```python
> re.findall(r"v(\d+\.\d+\.\d+)", text)
> ```
>
> Corrige la regex pour aussi capturer les suffixes `-beta.1`, `-rc.2`, `-alpha`. Teste mentalement sur `v1.2.3`, `v10.20.30`, `v2.0.0-rc.1`. Explique ce que tu changes.

## Réponse attendue

```json
{
  "expected_tokens": [
    "re.findall",
    "(?:-[0-9a-zA-Z.]+)?",
    "pre-release",
    "optional",
    "semver",
    "rc"
  ]
}
```

## Scoring

- **2** : ≥ 5/6 tokens (regex étendue + explication semver)
- **1** : 3-4/6
- **0** : < 3/6

## Notes pour le juge

Groupe optionnel `(?:-[0-9a-zA-Z.]+)?` à la fin. Accepte aussi la forme avec `|` (alternative) si elle couvre tous les cas. Regex qui casse sur `v10.20.30-rc.1-foo` autorisée (off-spec).
