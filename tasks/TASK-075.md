# TASK-075 — write-tests-edge-cases

**Catégorie** : writing_tests
**Difficulté** : medium
**Artefact(s) lié(s)** : —
**Type de scoring** : `contains_all`

## Prompt (envoyé à l'agent)

> La fonction `calculate_refund(order_total: float, returned_items_total: float, shipping: float = 0, *, refund_shipping: bool = False) -> float` doit retourner le montant à rembourser. Liste TOUS les edge cases à tester et écris le code pytest dans `tests/test_refund.py`. Au minimum :
> - refund_shipping False et True
> - returned_items_total = order_total (full refund)
> - returned_items_total = 0 (rien à rembourser)
> - returned_items_total > order_total (should raise ValueError)
> - floats arrondis à 0.01
> - shipping = 0
> - negative amounts (ValueError)

## Réponse attendue

```json
{
  "expected_tokens": [
    "def test_",
    "pytest.raises",
    "ValueError",
    "refund_shipping",
    "full_refund",
    "no_items",
    "exceeds",
    "round",
    "tests/test_refund.py"
  ]
}
```

## Scoring

- **2** : ≥ 7/9 tokens (≥ 6 edge cases couverts + raises + rounding)
- **1** : 4-6/9
- **0** : < 4/9

## Notes pour le juge

Test du cas "returned > order" doit utiliser `pytest.raises`. Sinon l'agent a raté la contrainte. Bonus si test des floats avec `pytest.approx`.
