# TASK-035 — bug-auth

**Catégorie** : debug
**Difficulté** : medium
**Artefact(s) lié(s)** : BUG-002
**Type de scoring** : `exact_match`

## Prompt (envoyé à l'agent)

> Un pentest a relevé que des mots de passe vides passent la validation d'authentification. Trouve le bug et explique-le.

## Réponse attendue

```json
{
  "file": "apps/api/utils/buggy_auth.py",
  "symbol": "buggy_verify_password",
  "bug_hint": "return True"
}
```

## Scoring

- **2** : fichier + symbole + ligne (±3) corrects
- **1** : fichier + symbole corrects, ligne hors tolérance
- **0** : symbole incorrect ou non trouvé

## Notes pour le juge

BUG-002 : buggy_verify_password renvoie True si l'un des deux est vide.
