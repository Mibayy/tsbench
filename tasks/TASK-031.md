# TASK-031 — explain-function-flow

**Catégorie** : explanation
**Difficulté** : medium
**Artefact(s) lié(s)** : —
**Type de scoring** : `llm_judge`

## Prompt (envoyé à l'agent)

> Explique en détail ce que fait la fonction `apply_discount` dans `apps/api/services/billing.py` : ses entrées, son effet de bord principal, ses dépendances externes (DB, logging, config), et les cas non couverts actuellement. Structure ta réponse : (1) signature + rôle, (2) effet de bord, (3) deps, (4) gaps de validation.

## Réponse attendue

```json
{
  "rubric": {
    "score_2_criteria": [
      "Identifie la signature `apply_discount(payload: dict, user_id: int = 0)` ET mentionne qu'elle retourne un dict `{ok, op, user}`",
      "Mentionne au moins 2 dépendances parmi : `_billing_admin_db()` / `supabase_admin` / `info()` logging / `settings`",
      "Identifie au moins 2 gaps : pas de validation du pourcentage de remise, pas de lecture réelle du payload, pas de persistence DB"
    ],
    "score_1_criteria": [
      "Identifie la signature + au moins 1 dep OU 1 gap, mais rate le reste"
    ],
    "score_0_criteria": [
      "Ne trouve pas la fonction OU donne une réponse générique sans citer le code"
    ]
  }
}
```

## Scoring

- **2** : les 3 critères score_2 remplis (juge Haiku)
- **1** : réponse partielle selon rubric
- **0** : miss complet

## Notes pour le juge

Réponse attendue riche — teste la capacité à lire du code avec padding synthétique et en extraire le vrai comportement. LLM-judge pondère sur la présence des éléments clés sans exiger des mots exacts.
