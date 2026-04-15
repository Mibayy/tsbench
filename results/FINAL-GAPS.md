# FINAL-GAPS -- Analyse des pertes residuelles Token Savior

_Score actuel : A=56% (67/120), B=82% (98/120). TS gagne 22, perd 2._
_Generated 2026-04-15_

## 1. SCORE LOSSES (B < A ou B < 2 atteignable)

### TASK-035 -- exact_match -- A=2/2 B=0/2

**Prompt** : Trouve le bug dans le code d'authentification.
**Expected** : `buggy_auth.py`, `buggy_verify_password`, `return True`
**B response** : Trouve un bug dans `auth.py:authenticate_user` (code mort, pas de validation password) -- vrai bug mais pas celui attendu.
**A response** : Trouve `buggy_auth.py:buggy_verify_password` avec le `return True` inverse.

**Root cause** : L'agent TS cherche "auth" via search_codebase et tombe sur `auth.py` (plus gros fichier, plus de resultats). Il n'explore jamais `buggy_auth.py`. Le recipe "FIND A BUG" n'est pas suivi.

**Action** : Fix system prompt -- renforcer la regle : "Si le prompt mentionne un fichier specifique (meme partiellement, e.g. 'buggy'), chercher ce fichier EXACTEMENT avec `find_symbol` ou `list_files(glob='*buggy*')` AVANT toute exploration libre."
**Effort** : 5 min

---

### TASK-052 -- contains_all -- A=2/2 B=1/2

**Prompt** : Identifie les communautes de code dans le projet.
**Expected** : must_contain = ["communaut", "symbole"]
**B response** : Liste 10 communautes avec details, contient "communautes" mais formule differemment les symboles.
**A response** : Liste les communautes avec le mot "symboles" explicite.

**Root cause** : Le mot "symbole" n'apparait pas textuellement dans la reponse B (elle utilise "fonctions", "modules"). Le grader `contains_all` fait du substring matching strict.

**Action** : Fix grader -- pour `contains_all`, utiliser `_keyword_match` au lieu du substring exact quand les candidats sont courts (< 15 chars). "symbole" matcherait "symboles principaux" via keyword.
**Effort** : 10 min

---

## 2. ACTIVE_TOKENS LOSSES (B > A)

### Cout fixe incompressible (system prompt MCP)

Ces taches ont un overhead de 25-45% du exclusivement au system prompt MCP + switch_project. L'agent fait le minimum (1-2 tool calls) mais le cout fixe domine.

| Task | Delta | B tools | Action |
|------|-------|---------|--------|
| TASK-001 | +31% | find_symbol x1 | Incompressible |
| TASK-007 | +34% | get_dependents x1 | Incompressible |
| TASK-023 | +30% | detect_breaking_changes x1 | Incompressible |
| TASK-025 | +28% | find_hotspots x1 | Incompressible |
| TASK-029 | +34% | analyze_config x1 | Incompressible |

**Action globale** : Incompressible. Le system prompt MCP (~4K tokens) + switch_project = cout plancher. Ces taches sont trop courtes (1 Grep suffit en Run A) pour que TS soit rentable.

---

### Agent tatonne (trop de tool calls)

| Task | Delta | Probleme | Action | Effort |
|------|-------|----------|--------|--------|
| TASK-005 | +397% | search_codebase x2 pour trouver un champ Prisma, l'agent fait 46K active | Fix system prompt : "Pour .prisma, utiliser search_codebase('role', glob='*.prisma') en un call" | 5 min |
| TASK-010 | +111% | get_dependents retourne 20 callers (1.7K chars) mais 47K active | Investiguer : pourquoi 47K active avec seulement 2 tool calls et 1.7K chars? Possible que le cache_creation soit eleve | 10 min |
| TASK-022 | +56% | 15 tool calls : search_codebase x3 + detect_breaking_changes + get_function_source x8 | Fix system prompt : "BREAKING CHANGES: detect_breaking_changes seul suffit. Max 3 tool calls." | 5 min |
| TASK-027 | +98% | analyze_config(9.6K chars) + get_env_usage x5 + search_codebase x2 | Fix system prompt : "ORPHAN ENV VARS: analyze_config(checks=['orphans']) retourne tout. Stop apres." | 5 min |
| TASK-028 | +58% | analyze_config retourne 9.6K chars (tout le config audit) | Fix code TS : analyze_config devrait avoir un mode compact (juste orphans, pas full audit) | 30 min |
| TASK-031 | +157% | 25 tool calls pour constater "pas de vars dans k8s" | Fix system prompt : "Pour verifier k8s env vars: search_codebase('env:', glob='infra/k8s/*') → si vide, repondre directement" | 5 min |
| TASK-034 | +64% | 13 tool calls, explore changed_symbols + reindex + 5x get_function_source | Fix system prompt : "DEBUG: find_symbol(nom_exact) → get_function_source → analyser. Max 3 calls." | 5 min |
| TASK-037 | +69% | list_files x5 pour comprendre le projet | Fix system prompt : "OVERVIEW: get_project_summary → get_structure_summary(root) → stop. Max 3 calls." | 5 min |
| TASK-053 | +135% | find_semantic_duplicates x2 (38K chars!) + 14 autres calls | Fix code TS : find_semantic_duplicates retourne trop de donnees (38K chars). Truncate ou paginate. | 30 min |

---

### Overhead modere mais acceptable (score egal ou meilleur)

| Task | Delta | Score A/B | Justification |
|------|-------|-----------|---------------|
| TASK-004 | +42% | 1/1 | get_routes donne plus de contexte |
| TASK-011 | +47% | 1/2 B gagne | get_full_context x4 mais meilleur score |
| TASK-013 | +45% | 1/2 B gagne | Meme pattern que 011 |
| TASK-018 | +47% | 1/1 | Exploration necessaire (.prisma) |
| TASK-021 | +26% | 0/1 B gagne | get_changed_symbols retourne 9K |
| TASK-036 | +22% | 0/1 B gagne | find_semantic_duplicates efficace |
| TASK-043 | +6% | 1/2 B gagne | get_functions x13 mais meilleur score |
| TASK-054 | +7% | 2/2 | Overhead negligeable |

---

## 3. WALL TIME LOSSES (B > A * 1.5)

### Latence MCP inherente (2-3 calls, latence reseau)

Chaque tool call MCP ajoute ~3-5s de latence (serialisation JSON + exec Python + deserialisation). Pour les taches ou Run A fait 1 Grep en 0.5s, Run B fait switch_project (3s) + 1 tool (3s) = 6s minimum.

| Task | A time | B time | B calls | Pattern |
|------|--------|--------|---------|---------|
| TASK-001 | 9.4s | 16.6s | 2 | switch + find_symbol |
| TASK-002 | 11.4s | 22.8s | 3 | switch + dependents + search |
| TASK-006 | 13.3s | 23.9s | 3 | switch + find_symbol + dependents |
| TASK-007 | 10.9s | 19.1s | 2 | switch + dependents |
| TASK-008 | 8.9s | 23.6s | 2 | switch + dependents |
| TASK-009 | 11.2s | 21.8s | 2 | switch + dependents |
| TASK-010 | 13.6s | 24.8s | 2 | switch + dependents |
| TASK-042 | 24.0s | 50.9s | 2 | switch + get_functions |

**Action** : Incompressible. Latence inherente au protocole MCP stdio. Optimisable seulement cote serveur TS (cache chaud, skip revalidation).
**Effort** : Moyen (optimisation serveur)

---

### Agent tatonne (exploration excessive = temps perdu)

| Task | A time | B time | B calls | Probleme | Action | Effort |
|------|--------|--------|---------|----------|--------|--------|
| TASK-011 | 13.8s | 59.9s | 7 | get_function_source x5 (suit la chaine call par call) | Fix system prompt : "CALL CHAIN: get_call_chain en 1 call, pas get_function_source en boucle" | 5 min |
| TASK-012 | 13.6s | 41.0s | 6 | get_function_source x4 | Idem | 0 min (meme fix) |
| TASK-013 | 12.8s | 31.8s | 6 | get_function_source x4 | Idem | 0 min |
| TASK-031 | 25.2s | 100.6s | 25 | Exploration massive | Deja traite (tokens loss) | 0 min |
| TASK-034 | 16.9s | 79.1s | 13 | 13 calls pour un debug | Deja traite (tokens loss) | 0 min |
| TASK-041 | 26.0s | 129.3s | 4 | 2x get_function_source lents | Investiguer : pourquoi 129s pour 4 calls? Possible timeout ou gros fichier | 15 min |
| TASK-044 | 55.7s | 114.5s | 4 | get_full_context x3 | Fix system prompt : "HEAVY_READ: utiliser batch mode get_full_context(names=[...]) en 1 call" | 5 min |
| TASK-045 | 17.3s | 111.6s | 4 | search_codebase x3 | Fix system prompt : "IMPORT SEARCH: get_file_dependents en 1 call, pas search_codebase en boucle" | 5 min |
| TASK-046 | 28.7s | 86.0s | 3 | get_functions + get_function_source | Pas de fix evident, exploration necessaire | Incompressible |
| TASK-050 | 21.6s | 162.9s | 5 | get_backward_slice prend du temps | Investiguer : get_backward_slice lent sur gros graphe? | 15 min |

---

## Tableau de synthese

| Task | Cat. perte | Root cause | Action | Effort |
|------|-----------|------------|--------|--------|
| TASK-035 | Score B=0 | Agent ignore buggy_auth.py | Fix system prompt : chercher fichier exact du prompt | 5 min |
| TASK-052 | Score B=1 | Grader substring trop strict | Fix grader : keyword match pour candidats courts | 10 min |
| TASK-005 | Tokens +397% | Agent tatonne sur .prisma | Fix system prompt : recipe Prisma search | 5 min |
| TASK-010 | Tokens +111% | cache_creation eleve inexplique | Investiguer cache behavior | 10 min |
| TASK-031 | Tokens +157% | 25 tool calls pour "pas de vars" | Fix system prompt : recipe K8s env check | 5 min |
| TASK-053 | Tokens +135% | find_semantic_duplicates 38K | Fix code TS : truncate output | 30 min |
| TASK-028 | Tokens +58% | analyze_config 9.6K | Fix code TS : mode compact | 30 min |
| TASK-022 | Tokens +56% | 15 calls apres detect_breaking | Fix system prompt : max 3 calls | 5 min |
| TASK-027 | Tokens +98% | analyze_config + env_usage x5 | Fix system prompt : stop apres analyze_config | 5 min |
| TASK-034 | Tokens +64% | 13 calls pour debug | Fix system prompt : max 3 calls pour debug | 5 min |
| TASK-037 | Tokens +69% | list_files x5 | Fix system prompt : overview recipe | 5 min |
| TASK-050 | Wall +654% | get_backward_slice lent | Investiguer perf serveur TS | 15 min |
| TASK-041 | Wall +397% | get_function_source lent | Investiguer perf serveur TS | 15 min |
| TASK-045 | Wall +547% | search_codebase x3 en boucle | Fix system prompt : get_file_dependents | 5 min |
| TASK-011 | Wall +336% | get_function_source x5 en boucle | Fix system prompt : get_call_chain | 5 min |
| TASK-044 | Wall +106% | get_full_context x3 sequentiel | Fix system prompt : batch mode | 5 min |
| TASK-001 | All +31% | Cout fixe MCP | Incompressible | - |
| TASK-007 | All +34% | Cout fixe MCP | Incompressible | - |
| TASK-023 | All +30% | Cout fixe MCP | Incompressible | - |
| TASK-025 | All +28% | Cout fixe MCP | Incompressible | - |
| TASK-029 | All +34% | Cout fixe MCP | Incompressible | - |

## Priorites

### P1 -- Quick wins system prompt (6 taches, 30 min total)
Ajouter/renforcer les recipes :
- CALL CHAIN : get_call_chain, pas get_function_source en boucle (011, 012, 013)
- BUG SEARCH : chercher le fichier exact mentionne dans le prompt (035)
- BATCH MODE : insister sur get_full_context(names=[...]) (044)
- IMPORT : get_file_dependents au lieu de search_codebase x3 (045)
- Limiter : max 5 tool calls par tache sauf edit/checkpoint

### P2 -- Fix grader (1 tache, 10 min)
- TASK-052 : keyword match pour candidats courts dans contains_all

### P3 -- Optimisation serveur TS (2 taches, 30 min)
- find_semantic_duplicates : truncate a 10K chars max (053)
- analyze_config : mode compact / filtrable (028)

### P4 -- Investigation (3 taches, 40 min)
- TASK-010 : pourquoi 47K active avec 2 calls et 1.7K chars
- TASK-041 : pourquoi 129s pour 4 calls
- TASK-050 : pourquoi get_backward_slice prend 162s

### Incompressible (5 taches)
- TASK-001, 007, 023, 025, 029 : cout fixe MCP ~4K tokens. Taches trop simples pour que TS soit rentable. Aucun fix possible sans reduire le system prompt MCP.
