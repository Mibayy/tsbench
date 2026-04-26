# TASK-090 — write-pr-description

**Catégorie** : git
**Difficulté** : medium
**Artefact(s) lié(s)** : —
**Type de scoring** : `llm_judge`

## Prompt (envoyé à l'agent)

> Examine les changements non-commités ou entre la branche actuelle et `main` (selon ce qui est le plus pertinent). Rédige une description de Pull Request complète en markdown avec les sections :
> - **Summary** (2-4 bullets du changement principal)
> - **Motivation** (pourquoi on fait ça)
> - **Changes** (liste des fichiers/zones touchés)
> - **Test plan** (comment reviewer peut valider)
> - **Risks / Backward compatibility** (ce qui peut casser)
>
> Ne rien inventer si l'info manque — indique "N/A" explicitement.

## Réponse attendue

```json
{
  "rubric": {
    "score_2_criteria": [
      "Les 5 sections présentes avec contenu non-trivial",
      "Changes liste au moins 2 fichiers/zones réels",
      "Test plan actionnable (commandes ou étapes concrètes, pas 'run tests')",
      "N/A explicite si une section n'a pas de contenu (pas inventé)"
    ],
    "score_1_criteria": ["3-4 sections complètes avec du contenu réel"],
    "score_0_criteria": ["Template vide / invente des changements"]
  }
}
```

## Scoring

- **2** : 4/4 critères juge
- **1** : 2-3/4
- **0** : 0-1/4

## Notes pour le juge

LLM-judge Haiku note la structure + la précision. Une réponse "template" avec sections vides ou "TBD" = 0.
