#!/usr/bin/env python3
"""Generate 40 benchmark task files + tasks/index.json from GROUND_TRUTH.json.

Each task is anchored on real artifact IDs so the expected answers stay in
sync with whatever generate.py + breaking_changes.py produce.
"""
from __future__ import annotations
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).parent.resolve()
GT = json.loads((ROOT / "GROUND_TRUTH.json").read_text())
ARTIFACTS: dict[str, dict] = {a["id"]: a for a in GT["artifacts"]}


def art(id_: str) -> dict:
    return ARTIFACTS[id_]


# -------------------------------------------------------------
# Scoring rubrics — one per kind, reused across tasks
# -------------------------------------------------------------
SCORING_RUBRICS = {
    "exact_match": """- **2** : fichier + symbole + ligne (±3) corrects
- **1** : fichier + symbole corrects, ligne hors tolérance
- **0** : symbole incorrect ou non trouvé""",
    "set_match_strict": """- **2** : liste exactement égale à la liste attendue (F1 = 1.0)
- **1** : F1 ≥ 0.75 (un ou deux éléments manquants ou en trop)
- **0** : F1 < 0.75""",
    "set_match_loose": """- **2** : la réponse contient au moins N éléments corrects parmi ceux attendus
- **1** : au moins la moitié des éléments attendus sont cités
- **0** : aucun élément correct""",
    "chain_match": """- **2** : chaîne complète dans le bon ordre
- **1** : tous les nœuds corrects mais ordre partiellement faux, ou un nœud manquant
- **0** : chaîne incorrecte ou incomplète (> 1 manquant)""",
    "boolean_with_evidence": """- **2** : oui/non correct ET citation des fichiers/symboles en preuve
- **1** : oui/non correct sans preuve concrète
- **0** : réponse incorrecte""",
    "free_form_rubric": """- **2** : couvre tous les points clés demandés, sans invention
- **1** : couvre la majorité des points mais en oublie ou invente un détail secondaire
- **0** : réponse incorrecte, très incomplète, ou hallucinations majeures""",
    "edit_quality": """- **2** : diff applicable, build/typecheck propre, tous les call sites mis à jour
- **1** : diff applicable mais un call site oublié ou un import cassé
- **0** : diff incorrect, ne compile pas, ou effet de bord non demandé""",
    "impact_set": """- **2** : liste exhaustive des dépendants (précision + rappel = 1.0)
- **1** : rappel ≥ 0.75 (quelques oublis tolérés)
- **0** : rappel < 0.75""",
}

TASKS: list[dict[str, Any]] = []


def add(
    id_: str,
    slug: str,
    category: str,
    difficulty: str,
    refs: list[str],
    prompt: str,
    expected: dict,
    scoring: str,
    notes: str = "",
) -> None:
    TASKS.append({
        "id": id_,
        "slug": slug,
        "category": category,
        "difficulty": difficulty,
        "ground_truth_refs": refs,
        "prompt": prompt,
        "expected": expected,
        "scoring": scoring,
        "notes": notes,
    })


# =============================================================
# CATÉGORIE 1 — Localisation (TASK-001..006)
# =============================================================
a = art("CALLER-001")
add(
    "TASK-001", "find-function", "localisation", "easy",
    ["CALLER-001"],
    "Dans ce projet, où est définie la fonction utilitaire `lonely_util` ? Donne-moi le fichier et la ligne.",
    {
        "file": a["target_file"],
        "symbol": a["target_symbol"],
        "line": a["target_line"],
    },
    "exact_match",
    "Symbole unique dans le projet — pas d'ambiguïté. Le fichier contient 4 fonctions utilitaires (lonely_util, small_util, medium_util, hub_util).",
)

a = art("CALLER-002")
add(
    "TASK-002", "find-callers", "localisation", "medium",
    ["CALLER-002"],
    "Liste tous les endroits qui appellent `small_util`. Je veux une liste exhaustive de fichiers.",
    {
        "symbol": a["target_symbol"],
        "expected_files": a["caller_files"],
        "count": a["caller_count"],
    },
    "set_match_strict",
    "3 callers exactement dans apps/api/callers/caller_small_util_*.py. Pas de faux positifs attendus.",
)

a = art("UNDECL-001")
add(
    "TASK-003", "find-env-usage", "localisation", "easy",
    ["UNDECL-001"],
    "Où est utilisée la variable d'environnement `SECRET_UNDECLARED_TOKEN` dans le code ? Donne-moi le fichier et la fonction.",
    {
        "env_var": a["env_var"],
        "file": a["file"],
        "function": "get_secret_config",
    },
    "exact_match",
    "Cette variable est lue mais pas déclarée dans .env.example (UNDECL). Une seule référence dans le code.",
)

add(
    "TASK-004", "find-route", "localisation", "easy",
    [],
    "Quel fichier handle la route `POST /api/billing` dans le backend ?",
    {
        "file": "apps/api/routers/billing.py",
        "handler": "create_billing",
        "method": "POST",
        "path": "/api/billing",
    },
    "exact_match",
    "Routes définies dans routers/billing.py via ROUTES.append tuples. Handler 'create_billing'.",
)

add(
    "TASK-005", "find-schema-field", "localisation", "easy",
    [],
    "Dans quelle table et quelle colonne est stocké le rôle d'un membre d'association ? Donne le fichier de schéma.",
    {
        "file": "packages/db/schema.prisma",
        "table": "Member",
        "column": "role",
    },
    "exact_match",
    "Schéma Prisma unique : packages/db/schema.prisma, model Member, champ role String.",
)

add(
    "TASK-006", "find-component-usage", "localisation", "medium",
    [],
    "Quels fichiers importent et utilisent le composant React `<Sidebar>` ?",
    {
        "component": "Sidebar",
        "imported_in_pattern": "apps/web/app/*/page.tsx",
        "min_expected_count": 15,
    },
    "set_match_loose",
    "Toutes les pages app/*/page.tsx importent Sidebar. ~15 pages + home.",
)


# =============================================================
# CATÉGORIE 2 — Dépendants / usages (TASK-007..010)
# =============================================================
for idx, caller_id, slug in [
    (7, "CALLER-001", "callers-exhaustive-1"),
    (8, "CALLER-002", "callers-exhaustive-3"),
    (9, "CALLER-003", "callers-exhaustive-8"),
    (10, "CALLER-004", "callers-exhaustive-20"),
]:
    a = art(caller_id)
    n = a["caller_count"]
    diff = "easy" if n <= 3 else ("medium" if n <= 8 else "hard")
    add(
        f"TASK-{idx:03d}", slug, "dépendants", diff,
        [caller_id],
        f"Donne-moi la liste complète et exhaustive des fichiers qui appellent la fonction `{a['target_symbol']}`. Je veux tous les call sites, pas un échantillon.",
        {
            "symbol": a["target_symbol"],
            "count": n,
            "expected_files": a["caller_files"],
        },
        "set_match_strict",
        f"Exactement {n} callers plantés. Test d'exhaustivité — un oubli = F1 < 1.",
    )


# =============================================================
# CATÉGORIE 3 — Call chains (TASK-011..013)
# =============================================================
for idx, chain_id, slug in [
    (11, "CHAIN-001", "chain-alpha"),
    (12, "CHAIN-002", "chain-beta"),
    (13, "CHAIN-003", "chain-gamma"),
]:
    a = art(chain_id)
    entry = a["chain"][0]
    add(
        f"TASK-{idx:03d}", slug, "call_chain", "medium",
        [chain_id],
        f"À partir de la fonction `{entry}`, retrace la chaîne d'appels complète jusqu'à la fonction feuille (celle qui ne délègue plus à personne).",
        {
            "chain": a["chain"],
            "file": a["file"],
            "depth": len(a["chain"]),
        },
        "chain_match",
        f"Chaîne à {len(a['chain'])} niveaux dans {a['file']}. Ordre important.",
    )


# =============================================================
# CATÉGORIE 4 — Impact analysis (TASK-014..016)
# =============================================================
a = art("CALLER-004")
add(
    "TASK-014", "breaking-signature", "impact", "hard",
    ["CALLER-004"],
    f"Je compte changer la signature de la fonction `{a['target_symbol']}` dans `{a['target_file']}` pour qu'elle prenne un seul argument `context: dict` au lieu de `payload: dict`. Liste exhaustivement ce qui casse ailleurs dans le projet.",
    {
        "symbol": a["target_symbol"],
        "file": a["target_file"],
        "affected_files": a["caller_files"],
        "affected_count": a["caller_count"],
    },
    "impact_set",
    "20 callers — test stress de l'analyse d'impact transitive. Aucun call site ne doit être oublié.",
)

a = art("CYCLE-001")
add(
    "TASK-015", "file-impact", "impact", "medium",
    ["CYCLE-001"],
    "Je m'apprête à modifier `apps/api/cycles/mod_a.py`. Quels fichiers du projet sont susceptibles d'être affectés en aval (directement ou transitivement) ?",
    {
        "source": "apps/api/cycles/mod_a.py",
        "min_expected_downstream": ["apps/api/cycles/mod_b.py"],
        "hint": "cycle présent entre mod_a et mod_b",
    },
    "set_match_loose",
    "Cycle planté : mod_a ↔ mod_b. Le bon agent détecte l'impact circulaire.",
)

add(
    "TASK-016", "test-impact", "impact", "medium",
    ["BREAK-001"],
    "Je viens de modifier la fonction `compute_invoice` dans `apps/api/services/billing.py`. Quels fichiers de test devrais-je rejouer en priorité ?",
    {
        "source_symbol": "compute_invoice",
        "source_file": "apps/api/services/billing.py",
        "expected_test_files": ["tests/test_billing.py"],
    },
    "set_match_loose",
    "Un seul test file couvre billing dans la suite générée.",
)


# =============================================================
# CATÉGORIE 5 — Structural edit (TASK-017..020)
# =============================================================
a = art("AMBIG-001")
add(
    "TASK-017", "rename-symbol", "edit", "hard",
    ["AMBIG-001"],
    "Renomme la fonction `create_user` définie dans `apps/api/ambig/mod1.py` en `create_regular_user`, en mettant à jour tous ses call sites. Attention : une autre fonction du même nom existe dans `apps/api/ambig/mod2.py` — elle ne doit PAS être touchée.",
    {
        "target_file": "apps/api/ambig/mod1.py",
        "before_symbol": "create_user",
        "after_symbol": "create_regular_user",
        "must_not_touch": "apps/api/ambig/mod2.py",
    },
    "edit_quality",
    "Test de précision sur symbole ambigu. Renommer mod2 est une erreur éliminatoire.",
)

add(
    "TASK-018", "add-field", "edit", "medium",
    [],
    "Ajoute un champ optionnel `archivedAt: DateTime?` au modèle `Member` dans `packages/db/schema.prisma`, puis propage-le aux types TypeScript correspondants dans `apps/web/types/member.ts`.",
    {
        "schema_file": "packages/db/schema.prisma",
        "model": "Member",
        "new_field": "archivedAt: DateTime?",
        "ts_file": "apps/web/types/member.ts",
    },
    "edit_quality",
    "Édition multi-fichier Python/SQL + TS. Validation : diff propre, type TS inclut archivedAt.",
)

add(
    "TASK-019", "extract-constant", "edit", "medium",
    ["BREAK-006"],
    "Plusieurs modules utilisent le nombre magique `20` comme taille de page par défaut. Extrais-le dans une constante `DEFAULT_PAGE_SIZE` centralisée et mets à jour tous les usages.",
    {
        "magic_number": 20,
        "constant_name": "DEFAULT_PAGE_SIZE",
        "min_files_touched": 2,
    },
    "edit_quality",
    "Concerne apps/api/config.py et apps/api/utils/pagination.py au minimum.",
)

a = art("DUP-002")
add(
    "TASK-020", "move-module", "edit", "hard",
    ["DUP-002"],
    "La fonction `slugify` dans `apps/api/utils/strings.py` devrait logiquement vivre dans `packages/utils/` pour pouvoir être réutilisée. Déplace-la là-bas et corrige tous les imports.",
    {
        "from_file": "apps/api/utils/strings.py",
        "to_file": "packages/utils/strings.py",
        "symbol": "slugify",
    },
    "edit_quality",
    "Lié à DUP-002 : il existe déjà un `to_slug` dupliqué dans packages/utils/slug_copy.py — l'agent peut optionnellement le consolider.",
)


# =============================================================
# CATÉGORIE 6 — Change review (TASK-021..023)
# =============================================================
break_ids = [f"BREAK-{i:03d}" for i in range(1, 7)]

add(
    "TASK-021", "diff-summary", "review", "medium",
    break_ids,
    "Résume symbole par symbole tous les changements entre le tag `v1` et le tag `v2`. Je veux une bullet list courte.",
    {
        "expected_changes": [
            {"id": "BREAK-001", "kind": "rename_function", "from": "compute_invoice", "to": "calculate_invoice"},
            {"id": "BREAK-002", "kind": "signature_change", "symbol": "authenticate_user"},
            {"id": "BREAK-003", "kind": "remove_function", "symbol": "bulk_import_members"},
            {"id": "BREAK-004", "kind": "type_change", "symbol": "MembersStatus"},
            {"id": "BREAK-005", "kind": "route_removed", "route": "DELETE /api/webhooks/{id}"},
            {"id": "BREAK-006", "kind": "default_change", "symbol": "DEFAULT_PAGE_SIZE"},
        ],
        "expected_count": 6,
    },
    "set_match_strict",
    "6 BREAK-* exactement. Oublier un seul = F1 < 1.",
)

add(
    "TASK-022", "pr-risk", "review", "hard",
    break_ids,
    "Parmi les changements entre v1 et v2, lesquels sont les plus risqués et méritent une review attentive avant merge ? Classe-les par criticité.",
    {
        "high_risk_expected": ["BREAK-002", "BREAK-003", "BREAK-005"],
        "rationale": "signature/remove/route removal = breaking pour consumers externes",
    },
    "set_match_loose",
    "Subjectif mais BREAK-002/003/005 sont objectivement les plus cassants (API contract).",
)

add(
    "TASK-023", "breaking-detection", "review", "medium",
    break_ids,
    "Y a-t-il des breaking changes d'API entre v1 et v2 ? Si oui, lesquels exactement ?",
    {
        "has_breaking": True,
        "expected_breaks": break_ids,
        "expected_count": 6,
    },
    "set_match_strict",
    "Les 6 BREAK-* doivent être cités nommément (ou par description équivalente).",
)


# =============================================================
# CATÉGORIE 7 — Dead code / hotspots (TASK-024..026)
# =============================================================
dead_ids = [f"DEAD-{i:03d}" for i in range(1, 13)]
dead_symbols = [art(d)["symbol"] for d in dead_ids]
add(
    "TASK-024", "dead-code-audit", "audit", "medium",
    dead_ids,
    "Donne-moi 5 fonctions exportées qui ne sont jamais appelées nulle part dans le projet.",
    {
        "min_count_requested": 5,
        "all_dead_symbols": dead_symbols,
        "scoring": "au moins 5 symboles parmi all_dead_symbols, 0 faux positif",
    },
    "set_match_loose",
    f"12 candidats au total. Liste complète: {', '.join(dead_symbols)}",
)

hotspot_ids = [f"HOTSPOT-{i:03d}" for i in range(1, 6)]
hotspots_ranked = sorted(
    [(art(h)["symbol"], art(h)["cyclomatic_complexity"], art(h)["file"]) for h in hotspot_ids],
    key=lambda x: -x[1],
)
add(
    "TASK-025", "hotspot-audit", "audit", "medium",
    hotspot_ids,
    "Trouve les 3 fonctions les plus complexes (plus haute complexité cyclomatique) du projet.",
    {
        "top3_expected": [{"symbol": s, "cyclomatic": c, "file": f} for s, c, f in hotspots_ranked[:3]],
    },
    "set_match_strict",
    f"Top 3 attendu : {', '.join(s for s, _, _ in hotspots_ranked[:3])} (complexités 15, 14, 14).",
)

add(
    "TASK-026", "cycle-detection", "audit", "medium",
    ["CYCLE-001", "CYCLE-002"],
    "Y a-t-il des dépendances circulaires (import cycles) dans ce projet ? Si oui, cite-les.",
    {
        "has_cycles": True,
        "expected_cycles": [
            art("CYCLE-001")["files"],
            art("CYCLE-002")["files"],
        ],
        "count": 2,
    },
    "set_match_strict",
    "2 cycles plantés : mod_a↔mod_b et mod_x→mod_y→mod_z→mod_x.",
)


# =============================================================
# CATÉGORIE 8 — Config audit (TASK-027..029)
# =============================================================
orphan_vars = [art(f"ORPHAN-{i:03d}")["env_var"] for i in range(1, 5)]
add(
    "TASK-027", "orphan-env", "config", "easy",
    [f"ORPHAN-{i:03d}" for i in range(1, 5)],
    "Liste les variables d'environnement déclarées dans les fichiers `.env.example` mais qui ne sont jamais lues dans le code.",
    {
        "expected_orphans": orphan_vars,
        "count": len(orphan_vars),
    },
    "set_match_strict",
    f"4 orphans plantés : {', '.join(orphan_vars)}",
)

undecl_vars = [art(f"UNDECL-{i:03d}")["env_var"] for i in range(1, 3)]
add(
    "TASK-028", "undecl-env", "config", "medium",
    [f"UNDECL-{i:03d}" for i in range(1, 3)],
    "Liste les variables d'environnement lues dans le code Python mais absentes de `config/.env.example`.",
    {
        "expected_undeclared": undecl_vars,
        "count": len(undecl_vars),
    },
    "set_match_strict",
    f"2 undeclared plantées : {', '.join(undecl_vars)} (dans apps/api/utils/secret_reader.py).",
)

secret_vars = [art(f"SECRET-{i:03d}")["env_var"] for i in range(1, 4)]
add(
    "TASK-029", "secret-detection", "config", "medium",
    [f"SECRET-{i:03d}" for i in range(1, 4)],
    "Y a-t-il des secrets (clés API, tokens, credentials) exposés dans les fichiers du dossier `config/` ?",
    {
        "expected_secrets": secret_vars,
        "file": "config/.env.staging",
        "count": len(secret_vars),
    },
    "set_match_strict",
    "3 secrets plantés dans .env.staging (valeurs obfusquées en placeholders pour GitHub push protection — la détection se fait par nom de variable).",
)


# =============================================================
# CATÉGORIE 9 — Docker / infra (TASK-030..031)
# =============================================================
add(
    "TASK-030", "dockerfile-audit", "infra", "easy",
    ["DOCKER-001", "DOCKER-002"],
    "Review les Dockerfiles dans `infra/docker/`. Quels sont les problèmes que tu vois ?",
    {
        "expected_issues": [
            {"id": "DOCKER-001", "file": "infra/docker/worker.Dockerfile", "issue": "uses python:latest base image"},
            {"id": "DOCKER-002", "file": "infra/docker/web.Dockerfile", "issue": "exposes unused ports 9229 and 6666"},
        ],
        "count": 2,
    },
    "set_match_strict",
    "3 Dockerfiles : api (propre), worker (latest tag), web (ports debug exposés).",
)

add(
    "TASK-031", "infra-consistency", "infra", "hard",
    [],
    "Toutes les variables d'environnement référencées dans les manifests Kubernetes (`infra/k8s/`) sont-elles bien déclarées dans `config/.env.example` ?",
    {
        "k8s_env_refs_found": [],
        "note": "les manifests k8s générés ne référencent aucune env var — trivialement cohérent",
        "expected_answer": "Aucune env var référencée dans k8s/, donc cohérent par vacuité.",
    },
    "boolean_with_evidence",
    "Tâche piège : les k8s YAML générés n'ont pas de env refs. La bonne réponse est 'aucun problème, rien à vérifier'. Hallucination = 0.",
)


# =============================================================
# CATÉGORIE 10 — Test selection (TASK-032..033)
# =============================================================
add(
    "TASK-032", "test-selection-unit", "testing", "easy",
    [],
    "Quels fichiers de test couvrent le module `apps/api/services/billing` ?",
    {
        "expected_test_files": ["tests/test_billing.py"],
        "source_module": "apps/api/services/billing.py",
    },
    "set_match_strict",
    "Un seul test file correspond.",
)

a = art("CHAIN-001")
add(
    "TASK-033", "test-selection-change", "testing", "medium",
    ["CHAIN-001"],
    f"Je m'apprête à modifier la fonction `{a['chain'][1]}` dans `{a['file']}`. Quels tests devrais-je rejouer en priorité ?",
    {
        "source": f"{a['file']}:{a['chain'][1]}",
        "expected_note": "aucun test unitaire ne couvre directement ce module — la bonne réponse est 'aucun test existant ne cible ce fichier, à créer'",
    },
    "free_form_rubric",
    "Aucun test ne couvre apps/api/chains/. Tâche piège : répondre 'tests/test_billing.py' au hasard = 0.",
)


# =============================================================
# CATÉGORIE 11 — Debug / reproduction (TASK-034..036)
# =============================================================
a = art("BUG-001")
add(
    "TASK-034", "bug-pagination", "debug", "medium",
    ["BUG-001"],
    "Un utilisateur signale que notre pagination retourne 11 résultats par page au lieu de 10. Où est le bug ?",
    {
        "file": a["file"],
        "symbol": a["symbol"],
        "bug_hint": a["expected_answer"]["bug_line_hint"],
    },
    "exact_match",
    "BUG-001 : off-by-one dans `buggy_paginate`, end index = start + page_size + 1.",
)

a = art("BUG-002")
add(
    "TASK-035", "bug-auth", "debug", "medium",
    ["BUG-002"],
    "Un pentest a relevé que des mots de passe vides passent la validation d'authentification. Trouve le bug et explique-le.",
    {
        "file": a["file"],
        "symbol": a["symbol"],
        "bug_hint": a["expected_answer"]["bug_line_hint"],
    },
    "exact_match",
    "BUG-002 : buggy_verify_password renvoie True si l'un des deux est vide.",
)

add(
    "TASK-036", "dup-detection", "debug", "hard",
    ["DUP-001", "DUP-002", "DUP-003"],
    "Y a-t-il des fonctions sémantiquement dupliquées dans ce projet ? Si oui, cite les paires que tu trouves.",
    {
        "expected_pairs": [
            [art("DUP-001")["pair"][0], art("DUP-001")["pair"][1]],
            [art("DUP-002")["pair"][0], art("DUP-002")["pair"][1]],
            [art("DUP-003")["pair"][0], art("DUP-003")["pair"][1]],
        ],
        "count": 3,
    },
    "set_match_strict",
    "3 paires : paginate/paginate_also, slugify/to_slug, start_of_day/day_start.",
)


# =============================================================
# CATÉGORIE 12 — Onboarding (TASK-037..038)
# =============================================================
add(
    "TASK-037", "project-overview", "onboarding", "easy",
    [],
    "En 10 bullet points maximum, explique ce que fait ce projet : quel domaine, quelles couches techniques, quels grands modules.",
    {
        "required_topics": [
            "SaaS / billing / members / sessions / webhooks",
            "FastAPI backend (apps/api)",
            "Next.js frontend (apps/web)",
            "Python worker (apps/worker)",
            "packages/ monorepo (shared-types, db, utils)",
            "Prisma schema (packages/db/schema.prisma)",
            "Docker + k8s + terraform infra",
        ],
        "max_bullets": 10,
    },
    "free_form_rubric",
    "Test d'économie de tokens : un bon agent doit éviter de lire tous les 290 fichiers.",
)

add(
    "TASK-038", "module-overview", "onboarding", "medium",
    [],
    "Explique l'architecture du module `apps/api/services/billing.py` : quelles sont ses responsabilités, ses fonctions principales, et ses dépendances ?",
    {
        "module": "apps/api/services/billing.py",
        "key_functions": ["compute_invoice", "apply_discount", "charge_customer", "refund_payment"],
        "dependencies": ["apps/api/db", "apps/api/models/billing", "apps/api/config", "apps/api/utils/logging"],
    },
    "free_form_rubric",
    "Réponse correcte mentionne les fonctions principales et les imports. v2 : compute_invoice est renommé en calculate_invoice.",
)


# =============================================================
# CATÉGORIE 13 — Cross-language (TASK-039..040)
# =============================================================
add(
    "TASK-039", "ts-py-type-mapping", "cross-language", "hard",
    [],
    "Le type TypeScript `Members` déclaré dans `packages/shared-types/members.ts` correspond à quel modèle Python dans le backend ? Donne le fichier et le nom de la classe.",
    {
        "ts_type": "Members",
        "ts_file": "packages/shared-types/members.ts",
        "py_class": "Member",
        "py_file": "apps/api/models/members.py",
    },
    "exact_match",
    "Cross-langage : Token Savior ne suit pas les liens cross-langage, la correspondance est par convention de nom.",
)

add(
    "TASK-040", "config-consistency", "cross-language", "hard",
    [],
    "Les champs déclarés dans `config/app.config.yaml` (app.name, features.billing, pagination.default, etc.) sont-ils tous effectivement consommés quelque part dans le code ?",
    {
        "config_file": "config/app.config.yaml",
        "expected_answer": "Aucun champ du YAML n'est effectivement lu par le code généré — le fichier existe mais n'est parsé nulle part.",
        "note": "tâche piège : le fichier YAML est un leurre, seules les env vars sont lues",
    },
    "boolean_with_evidence",
    "Hallucination test : un agent qui invente un loader YAML = 0.",
)


# =============================================================
# Render + write
# =============================================================
def render(t: dict) -> str:
    refs = ", ".join(t["ground_truth_refs"]) if t["ground_truth_refs"] else "—"
    expected_json = json.dumps(t["expected"], indent=2, ensure_ascii=False)
    rubric = SCORING_RUBRICS[t["scoring"]]
    md = f"""# {t["id"]} — {t["slug"]}

**Catégorie** : {t["category"]}
**Difficulté** : {t["difficulty"]}
**Artefact(s) lié(s)** : {refs}
**Type de scoring** : `{t["scoring"]}`

## Prompt (envoyé à l'agent)

> {t["prompt"]}

## Réponse attendue

```json
{expected_json}
```

## Scoring

{rubric}
"""
    if t["notes"]:
        md += f"\n## Notes pour le juge\n\n{t['notes']}\n"
    return md


def main() -> int:
    tasks_dir = ROOT / "tasks"
    tasks_dir.mkdir(exist_ok=True)

    assert len(TASKS) == 40, f"Expected 40 tasks, got {len(TASKS)}"

    for t in TASKS:
        (tasks_dir / f"{t['id']}.md").write_text(render(t))

    index = [
        {
            "id": t["id"],
            "slug": t["slug"],
            "category": t["category"],
            "difficulty": t["difficulty"],
            "ground_truth_refs": t["ground_truth_refs"],
            "scoring": t["scoring"],
        }
        for t in TASKS
    ]
    (tasks_dir / "index.json").write_text(json.dumps(index, indent=2) + "\n")

    # Per-category summary
    by_cat: dict[str, int] = {}
    for t in TASKS:
        by_cat[t["category"]] = by_cat.get(t["category"], 0) + 1

    print(f"Generated {len(TASKS)} tasks in {tasks_dir}")
    print("By category:")
    for cat, n in sorted(by_cat.items()):
        print(f"  {cat:20s} {n}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
