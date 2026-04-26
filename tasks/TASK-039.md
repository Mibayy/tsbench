# TASK-039 — infra-consistency

**Catégorie** : infra
**Difficulté** : hard
**Artefact(s) lié(s)** : —
**Type de scoring** : `boolean_with_evidence`

## Prompt (envoyé à l'agent)

> Toutes les variables d'environnement référencées dans les manifests Kubernetes (`infra/k8s/`) sont-elles bien déclarées dans `config/.env.example` ?

## Réponse attendue

```json
{
  "k8s_env_refs_found": [],
  "note": "les manifests k8s générés ne référencent aucune env var — trivialement cohérent",
  "expected_answer": "Aucune env var référencée dans k8s/, donc cohérent par vacuité."
}
```

## Scoring

- **2** : oui/non correct ET citation des fichiers/symboles en preuve
- **1** : oui/non correct sans preuve concrète
- **0** : réponse incorrecte

## Notes pour le juge

Tâche piège : les k8s YAML générés n'ont pas de env refs. La bonne réponse est 'aucun problème, rien à vérifier'. Hallucination = 0.
