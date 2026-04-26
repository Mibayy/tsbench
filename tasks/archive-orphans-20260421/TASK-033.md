# TASK-033 — test-selection-change

**Catégorie** : testing
**Difficulté** : medium
**Artefact(s) lié(s)** : CHAIN-001
**Type de scoring** : `free_form_rubric`

## Prompt (envoyé à l'agent)

> Je m'apprête à modifier la fonction `alpha_middle` dans `apps/api/chains/alpha.py`. Quels tests devrais-je rejouer en priorité ?

## Réponse attendue

```json
{
  "source": "apps/api/chains/alpha.py:alpha_middle",
  "expected_note": "aucun test unitaire ne couvre directement ce module — la bonne réponse est 'aucun test existant ne cible ce fichier, à créer'"
}
```

## Scoring

- **2** : couvre tous les points clés demandés, sans invention
- **1** : couvre la majorité des points mais en oublie ou invente un détail secondaire
- **0** : réponse incorrecte, très incomplète, ou hallucinations majeures

## Notes pour le juge

Aucun test ne couvre apps/api/chains/. Tâche piège : répondre 'tests/test_billing.py' au hasard = 0.
