# TASK-085 — write-docstring-function

**Catégorie** : documentation
**Difficulté** : easy
**Artefact(s) lié(s)** : —
**Type de scoring** : `llm_judge`

## Prompt (envoyé à l'agent)

> Écris une docstring Google-style complète pour la fonction `apply_discount(payload: dict, user_id: int = 0)` de `apps/api/services/billing.py`. La docstring doit contenir : description, Args (avec types), Returns, Raises, Example. Ne modifie PAS le code, uniquement donne la docstring à insérer sous la signature.

## Réponse attendue

```json
{
  "rubric": {
    "score_2_criteria": [
      "Format Google-style correct : description + sections Args/Returns/Raises/Example",
      "Args couvre les 2 paramètres avec leur type",
      "Returns décrit la structure du dict retourné",
      "Example syntaxiquement valide (avec >>> prompts)"
    ],
    "score_1_criteria": ["3/4 sections présentes mais description superficielle"],
    "score_0_criteria": ["Docstring 1 ligne ou format NumPy/Sphinx au lieu de Google"]
  }
}
```

## Scoring

- **2** : 4/4 critères juge
- **1** : 2-3/4
- **0** : 0-1/4

## Notes pour le juge

Google-style : `Args:` pas `Arguments:`, chaque param sur sa ligne avec 4 espaces d'indent. L'Example doit utiliser `>>>` interactifs.
