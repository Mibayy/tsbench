# TASK-067 — bug-fix-rounding

**Catégorie** : bug_fixing
**Difficulté** : medium
**Artefact(s) lié(s)** : —
**Type de scoring** : `contains_all`

## Prompt (envoyé à l'agent)

> La facturation produit parfois des totaux à `0.01` près de la somme des lignes :
>
> ```python
> def invoice_total(items: list[dict]) -> float:
>     subtotal = sum(item["price"] for item in items)
>     tax = subtotal * 0.20
>     return round(subtotal + tax, 2)
> ```
>
> Identifie la source de l'écart. Donne un fix robuste avec `decimal.Decimal`. Précise pourquoi `float` n'est pas adapté à du monétaire et mentionne la règle `ROUND_HALF_EVEN` vs `ROUND_HALF_UP`.

## Réponse attendue

```json
{
  "expected_tokens": [
    "Decimal",
    "float",
    "precision",
    "ROUND_HALF_UP",
    "quantize",
    "0.01",
    "monetary",
    "bankers"
  ]
}
```

## Scoring

- **2** : ≥ 6/8 tokens (Decimal + quantize + règle d'arrondi)
- **1** : 3-5/8
- **0** : < 3/8

## Notes pour le juge

Le default Decimal est ROUND_HALF_EVEN (bankers' rounding) — comptable français veut ROUND_HALF_UP. `.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)`.
