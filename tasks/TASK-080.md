# TASK-080 — write-tests-mock-dependency

**Catégorie** : writing_tests
**Difficulté** : medium
**Artefact(s) lié(s)** : —
**Type de scoring** : `contains_all`

## Prompt (envoyé à l'agent)

> Pour la fonction `send_welcome_email(user_id: int)` qui dépend de `db.get_user(user_id)` et `mailer.send(to, subject, body)`, écris 3 tests avec `pytest-mock` (`mocker`) :
> 1. User trouvé → mailer.send appelé avec les bons args (use `assert_called_once_with`)
> 2. User introuvable → mailer.send **pas** appelé (use `assert_not_called`)
> 3. mailer.send lève → propagation de l'exception

## Réponse attendue

```json
{
  "expected_tokens": [
    "mocker.patch",
    "assert_called_once_with",
    "assert_not_called",
    "side_effect",
    "pytest.raises",
    "return_value",
    "mock_mailer",
    "tests/test_welcome_email.py"
  ]
}
```

## Scoring

- **2** : ≥ 6/8 tokens (3 tests distincts + assert_called + assert_not_called + side_effect)
- **1** : 3-5/8
- **0** : < 3/8

## Notes pour le juge

`assert_called_once_with` est le bon assert (vs `assert mock.called` qui est trop laxe). Piège : mock le mailer mais oublier de mock `db.get_user`.
