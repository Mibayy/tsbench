# TASK-084 — security-review-auth

**Catégorie** : code_review
**Difficulté** : hard
**Artefact(s) lié(s)** : —
**Type de scoring** : `llm_judge`

## Prompt (envoyé à l'agent)

> Effectue une security review du module d'auth dans `apps/api/services/auth.py` et `apps/api/services/complex_auth.py`. Liste les vulnérabilités potentielles (OWASP-style). Pour chaque vulnérabilité :
> - Type (A01 Broken Access Control, A02 Crypto, A07 Auth failures, etc.)
> - Fichier:ligne précis
> - Impact si exploité
> - Correctif proposé

## Réponse attendue

```json
{
  "rubric": {
    "score_2_criteria": [
      "Identifie au moins 3 vulnérabilités distinctes",
      "Cite un fichier:ligne précis pour chaque",
      "Classe au moins 2 selon OWASP Top 10",
      "Propose un correctif concret (pas générique) pour chaque"
    ],
    "score_1_criteria": ["2 vulnérabilités OU 3 sans classification OWASP"],
    "score_0_criteria": ["Vue générique sans citer le code, ou moins de 2 vulns"]
  }
}
```

## Scoring

- **2** : 4/4 critères
- **1** : 2-3/4
- **0** : 0-1/4

## Notes pour le juge

Vulnérabilités typiques à chasser : comparaison de secrets avec `==` au lieu de `compare_digest`, JWT sans vérification signature, sessions sans rotation, timing attacks sur login, SQL/NoSQL injection dans les lookups.
