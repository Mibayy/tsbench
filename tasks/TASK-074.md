# TASK-074 — write-tests-for-slugify

**Catégorie** : writing_tests
**Difficulté** : easy
**Artefact(s) lié(s)** : —
**Type de scoring** : `contains_all`

## Prompt (envoyé à l'agent)

> Écris des tests pytest pour une fonction `slugify(text: str) -> str` qui doit :
> - lowercase
> - espaces → `-`
> - retirer accents (é→e)
> - collapse tirets consécutifs
> - strip tirets en bord
>
> Couvre au moins 6 cas : simple, avec accents, multi-espaces, trailing spaces, string vide, caractères spéciaux (`&%`).
>
> **Important** : réponds avec le code complet du fichier `tests/test_slugify.py` dans un bloc markdown ```python ... ```, pas juste un résumé. Ne crée pas le fichier sur disque.

## Réponse attendue

```json
{
  "expected_tokens": [
    "import",
    "slugify",
    "def test",
    "assert",
    "parametrize",
    "test_slugify",
    "é",
    "\"\""
  ]
}
```

## Scoring

- **2** : ≥ 6/8 tokens (au moins 5 cas distincts + paramétrisation OU 6 tests séparés)
- **1** : 3-5/8
- **0** : < 3/8

## Notes pour le juge

`pytest.mark.parametrize` idéal pour cette tâche. Accepter aussi des tests séparés s'ils sont clairs. Refuser les tests qui ne couvrent que le happy path.
