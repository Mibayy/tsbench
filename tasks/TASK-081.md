# TASK-081 — explain-auth-middleware

**Catégorie** : explanation
**Difficulté** : medium
**Artefact(s) lié(s)** : —
**Type de scoring** : `llm_judge`

## Prompt (envoyé à l'agent)

> Explique le fonctionnement de la fonction/middleware d'auth dans `apps/api/services/auth.py`. Structure ta réponse :
> 1. Quelle stratégie d'auth (JWT / session / Bearer) ?
> 2. Où est extrait le token ? (header, cookie, query param)
> 3. Quelles validations sont faites (signature, expiration, scope) ?
> 4. Que fait le middleware en cas d'auth invalide ?

## Réponse attendue

```json
{
  "rubric": {
    "score_2_criteria": [
      "Identifie la stratégie d'auth (JWT/Bearer/session) OU documente l'absence d'implémentation réelle (scaffold/stub) en citant le fichier",
      "Explique où le token est récupéré OU note explicitement qu'aucune extraction n'est faite en citant une signature/ligne",
      "Liste au moins 2 validations effectuées OU constate l'absence de validations en citant le code (ex: seul check booléen, return hardcodé)",
      "Décrit le comportement en cas d'échec (401, raise, silent, ou 'retourne toujours ok' si scaffold) avec citation"
    ],
    "score_1_criteria": ["Couvre 2-3 des 4 points OU couvre les 4 sans citation de fichier"],
    "score_0_criteria": ["Réponse générique sans citer le code, ou invente des comportements qui n'existent pas"]
  }
}
```

## Scoring

- **2** : 4/4 critères remplis selon juge
- **1** : 2-3/4
- **0** : 0-1/4

## Notes pour le juge

Nécessite de lire apps/api/services/auth.py (~200 lignes). Test de capacité à naviguer + synthétiser. LLM-judge Haiku lira la réponse ET le fichier si besoin — mais en pratique juste la rubric.
