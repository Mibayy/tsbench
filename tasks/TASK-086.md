# TASK-086 — write-module-readme

**Catégorie** : documentation
**Difficulté** : medium
**Artefact(s) lié(s)** : —
**Type de scoring** : `llm_judge`

## Prompt (envoyé à l'agent)

> Rédige un README.md pour le module `packages/utils/` de ce projet. Il doit contenir :
> - Purpose (1 paragraphe)
> - Installation (si applicable)
> - Quick Start avec 2 exemples de code
> - Module contents : liste des fichiers principaux avec 1 phrase chacun
> - Contributing (1 paragraphe court)
>
> Sort le markdown brut, prêt à sauvegarder.

## Réponse attendue

```json
{
  "rubric": {
    "score_2_criteria": [
      "Les 5 sections (Purpose/Install/Quick Start/Contents/Contributing) présentes",
      "Quick Start contient 2 exemples de code valides avec syntaxe markdown ```python",
      "Module contents liste ≥ 4 vrais fichiers de packages/utils/",
      "Ton cohérent et markdown bien formaté (headings ##, listes)"
    ],
    "score_1_criteria": ["3-4 sections présentes avec exemples OU fichiers réels"],
    "score_0_criteria": ["Template générique sans lien au projet, ou fichiers inventés"]
  }
}
```

## Scoring

- **2** : 4/4 critères
- **1** : 2-3/4
- **0** : 0-1/4

## Notes pour le juge

Test de capacité à naviguer le module (lister fichiers réels) + produire de la doc structurée. Si l'agent hallucine des fichiers absents = 0.
