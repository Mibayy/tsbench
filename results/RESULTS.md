# tsbench — RESULTS

_Generated 2026-04-15T13:14:27.248184+00:00_

## 0. Notes sur cette itération

Résultats après implémentation de six améliorations issues de `IMPROVEMENT-SIGNALS.md` :

- **C1** `get_full_context` (source + callers + deps en un appel) — adoption : **9 tasks sur 60** après ajout du hint trailer sur `get_function_source` (C6). Avant C6 : 0 adoption.
- **C2** hints sur `find_symbol` / `get_functions` / `get_classes` → probable cause de la baisse de retries sur TASK-041 (15→8 au premier rerun).
- **C3** marker descriptif pour `get_imports` vide — bruit de signal (la plupart des cas "empty" étaient des outputs compressés valides).
- **C4** résolveur d'imports `from pkg import submod` → désormais pointe vers `pkg/submod.py` au lieu de `pkg/__init__.py`. Rend les cycles visibles dans l'import graph (TASK-026).
- **C5** grader fix pour `expected_cycles` — TASK-026 passé de 0 à **2/2** (réponse correcte mais clé non reconnue avant).
- **C6** hint trailer `→ get_full_context(...)` sur `get_function_source` / `get_class_source`.

**TASK-022 reste à 0/2** : c'est un _échec de reasoning_, pas une limitation Token Savior. L'agent a appelé `detect_breaking_changes` (848 chars utiles) puis a choisi d'explorer `billing.py`, `buggy_paginate`, `ambig/` — tous hors ground truth. Les fichiers attendus (`auth.py`, `members.py`, `webhooks.py`) n'ont jamais été visités malgré la donnée disponible. Aucun outil TS ne corrige un agent qui ignore son propre output.

## 1. Résumé exécutif

_Métrique principale : `active_tokens` = input + output + cache_creation (cache_read exclu — contexte réutilisé, proxy du coût quota abonnement)._

- **Tâches appariées** : 21
- **Réduction active_tokens A→B** : -15.1% (379,884 → 437,163)
- **Turns cumulés** : A=102 · B=144
- **Score global A** : 29/42 (69%)
- **Score global B** : 32/42 (76%)
- **Token Savior** : gagne 5, ex æquo 14, perd 2

## 2. Tableau principal

| Task | Catégorie | Active A | Active B | ΔActive | Chars A | Chars B | ΔChars | Score A | Score B |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| TASK-001 | localisation | 9080 | 44767 | -393% | 1,761 | 121 | +93% | 2/2 | 2/2 |
| TASK-002 | localisation | 17679 | 11500 | +35% | 1,737 | 350 | +80% | 2/2 | 2/2 |
| TASK-003 | localisation | 17037 | 45415 | -167% | 280 | 1,789 | -539% | 1/2 | 1/2 |
| TASK-004 | localisation | 9427 | 45256 | -380% | 558 | 1,296 | -132% | 1/2 | 1/2 |
| TASK-005 | localisation | 9331 | 14835 | -59% | 720 | 2,203 | -206% | 1/2 | 0/2 |
| TASK-006 | localisation | 21869 | 46529 | -113% | 986 | 3,762 | -282% | 0/2 | 0/2 |
| TASK-007 | dépendants | 9136 | 12487 | -37% | 1,761 | 2,672 | -52% | 2/2 | 2/2 |
| TASK-008 | dépendants | 18033 | 11543 | +36% | 3,227 | 350 | +89% | 2/2 | 2/2 |
| TASK-009 | dépendants | 44160 | 11980 | +73% | 5,231 | 757 | +86% | 2/2 | 2/2 |
| TASK-010 | dépendants | 22492 | 12920 | +43% | 12,668 | 1,786 | +86% | 2/2 | 2/2 |
| TASK-011 | call_chain | 9220 | 12902 | -40% | 1,364 | 1,961 | -44% | 1/2 | 2/2 |
| TASK-012 | call_chain | 21860 | 17503 | +20% | 1,327 | 1,922 | -45% | 1/2 | 2/2 |
| TASK-013 | call_chain | 9192 | 13134 | -43% | 1,364 | 1,961 | -44% | 1/2 | 2/2 |
| TASK-014 | impact | 27232 | 14860 | +45% | 12,668 | 7,893 | +38% | 2/2 | 0/2 |
| TASK-015 | impact | 9906 | 12698 | -28% | — | 360 | — | 0/2 | 0/2 |
| TASK-016 | impact | — | 11555 | — | — | 251 | — | — | 0/2 |
| TASK-017 | edit | — | 16095 | — | — | 4,345 | — | — | 2/2 |
| TASK-018 | edit | — | 13188 | — | — | 1,357 | — | — | 1/2 |
| TASK-019 | edit | — | 20044 | — | — | 16,817 | — | — | 2/2 |
| TASK-020 | edit | — | 17011 | — | — | 4,127 | — | — | 1/2 |
| TASK-021 | review | — | 14587 | — | — | 8,639 | — | — | 0/2 |
| TASK-022 | review | — | 22275 | — | — | 13,892 | — | — | 0/2 |
| TASK-023 | review | — | 6986 | — | — | 5,271 | — | — | 2/2 |
| TASK-024 | audit | — | 11888 | — | — | 440 | — | — | 0/2 |
| TASK-025 | audit | — | 5109 | — | — | 382 | — | — | 0/2 |
| TASK-026 | audit | — | 7075 | — | — | 1,237 | — | — | 2/2 |
| TASK-027 | config | — | 12058 | — | — | 15,180 | — | — | 0/2 |
| TASK-028 | config | — | 9811 | — | — | 8,257 | — | — | 0/2 |
| TASK-029 | config | — | 8619 | — | — | 8,063 | — | — | 0/2 |
| TASK-030 | infra | — | 5271 | — | — | 339 | — | — | 0/2 |
| TASK-031 | infra | — | 35519 | — | — | 43,526 | — | — | 0/2 |
| TASK-032 | testing | — | 4965 | — | — | 140 | — | — | 0/2 |
| TASK-033 | testing | — | 7783 | — | — | 3,206 | — | — | 0/2 |
| TASK-034 | debug | — | 8790 | — | — | 3,652 | — | — | 2/2 |
| TASK-035 | debug | — | 6277 | — | — | 3,847 | — | — | 2/2 |
| TASK-036 | debug | — | 12346 | — | — | 11,594 | — | — | 0/2 |
| TASK-037 | onboarding | — | 12335 | — | — | 4,429 | — | — | 0/2 |
| TASK-038 | onboarding | — | 8112 | — | — | 3,494 | — | — | 0/2 |
| TASK-039 | cross-language | — | 5765 | — | — | 689 | — | — | 0/2 |
| TASK-040 | cross-language | — | 13820 | — | — | 17,452 | — | — | 0/2 |
| TASK-041 | heavy_read | 33525 | 10616 | +68% | 23,633 | 9,396 | +60% | 2/2 | 2/2 |
| TASK-042 | heavy_read | 18667 | 13670 | +27% | 18,895 | 4,618 | +76% | 2/2 | 2/2 |
| TASK-043 | heavy_read | 19531 | 26573 | -36% | 196,882 | 16,264 | +92% | 1/2 | 2/2 |
| TASK-044 | heavy_read | 23485 | 16308 | +31% | 30,789 | 9,576 | +69% | 2/2 | 2/2 |
| TASK-045 | heavy_read | 8497 | 23654 | -178% | 14 | 2,159 | -15321% | 0/2 | 2/2 |
| TASK-046 | heavy_read | 20525 | 18013 | +12% | 20,258 | 8,762 | +57% | 2/2 | 2/2 |
| TASK-047 | navigation | — | 11611 | — | — | 180 | — | — | 2/2 |
| TASK-048 | navigation | — | 11896 | — | — | 631 | — | — | 2/2 |
| TASK-049 | call_chain | — | 11707 | — | — | 301 | — | — | 2/2 |
| TASK-050 | navigation | — | 13146 | — | — | 2,047 | — | — | 1/2 |
| TASK-051 | navigation | — | 13642 | — | — | 4,989 | — | — | 2/2 |
| TASK-052 | audit | — | 15484 | — | — | 3,709 | — | — | 2/2 |
| TASK-053 | audit | — | 19676 | — | — | 11,025 | — | — | 2/2 |
| TASK-054 | edit | — | 48290 | — | — | 2,506 | — | — | 2/2 |
| TASK-055 | edit | — | 45021 | — | — | 353 | — | — | 2/2 |
| TASK-056 | edit | — | 52964 | — | — | 7,587 | — | — | 2/2 |
| TASK-057 | testing | — | 11834 | — | — | 239 | — | — | 2/2 |
| TASK-058 | audit | — | 15412 | — | — | 6,091 | — | — | 2/2 |
| TASK-059 | git | — | 12472 | — | — | 1,608 | — | — | 2/2 |
| TASK-060 | git | — | 13647 | — | — | 4,374 | — | — | 2/2 |

## 3. Moyennes par catégorie

| Catégorie | N | Active A moy | Active B moy | Réduction | Turns A moy | Turns B moy | Score A moy | Score B moy |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| call_chain | 3 | 13,424 | 14,513 | -8% | 4.3 | 7.0 | 1.00 | 2.00 |
| dépendants | 4 | 23,455 | 12,232 | +48% | 2.0 | 3.8 | 2.00 | 2.00 |
| heavy_read | 6 | 20,705 | 18,139 | +12% | 6.8 | 9.8 | 1.50 | 2.00 |
| impact | 2 | 18,569 | 13,779 | +26% | 9.0 | 8.0 | 1.00 | 0.00 |
| localisation | 6 | 14,070 | 34,717 | -147% | 3.7 | 5.5 | 1.17 | 1.00 |

## 3bis. Analyse chars_injected (ce que TS prétend économiser)

- **Pairs mesurés** : 20
- **Chars injectés cumulés** : A=336,123 · B=79,598 · Δ=+76%
- **TS gagne sur chars** : 11/20
- **TS perd sur chars** : 9/20
- **Ex æquo** : 0/20

### Tâches où TS gagne sur chars_injected

- **TASK-043** — chars 196,882→16,264 (-92%) | active 19,531→26,573 (+36%)
- **TASK-044** — chars 30,789→9,576 (-69%) | active 23,485→16,308 (-31%)
- **TASK-042** — chars 18,895→4,618 (-76%) | active 18,667→13,670 (-27%)
- **TASK-041** — chars 23,633→9,396 (-60%) | active 33,525→10,616 (-68%)
- **TASK-046** — chars 20,258→8,762 (-57%) | active 20,525→18,013 (-12%)
- **TASK-010** — chars 12,668→1,786 (-86%) | active 22,492→12,920 (-43%)
- **TASK-014** — chars 12,668→7,893 (-38%) | active 27,232→14,860 (-45%)
- **TASK-009** — chars 5,231→757 (-86%) | active 44,160→11,980 (-73%)
- **TASK-008** — chars 3,227→350 (-89%) | active 18,033→11,543 (-36%)
- **TASK-001** — chars 1,761→121 (-93%) | active 9,080→44,767 (+393%)
- **TASK-002** — chars 1,737→350 (-80%) | active 17,679→11,500 (-35%)

### Tâches où TS perd sur chars_injected

- **TASK-006** — chars 986→3,762 (+282%) | active 21,869→46,529 (+113%)
- **TASK-045** — chars 14→2,159 (+15321%) | active 8,497→23,654 (+178%)
- **TASK-003** — chars 280→1,789 (+539%) | active 17,037→45,415 (+167%)
- **TASK-005** — chars 720→2,203 (+206%) | active 9,331→14,835 (+59%)
- **TASK-007** — chars 1,761→2,672 (+52%) | active 9,136→12,487 (+37%)
- **TASK-004** — chars 558→1,296 (+132%) | active 9,427→45,256 (+380%)
- **TASK-011** — chars 1,364→1,961 (+44%) | active 9,220→12,902 (+40%)
- **TASK-013** — chars 1,364→1,961 (+44%) | active 9,192→13,134 (+43%)
- **TASK-012** — chars 1,327→1,922 (+45%) | active 21,860→17,503 (-20%)

### Break-even analysis

_Coût fixe B = active_tokens B − chars_injected B (baseline TS : system prompt, schémas ToolSearch). Gain chars = chars_A − chars_B. TS rentable sur active_tokens si : (active_A − active_B) ≥ 0, i.e. le gain chars_injected doit couvrir le surcoût baseline._

- **Surcoût moyen active_tokens B − A** : +2,724 tokens / tâche
- **Cas où B ≤ A sur active** : 10/20

| Task | Gain chars (A−B) | Surcoût active (B−A) |
|---|---:|---:|
| TASK-043 | +180,618 | +7,042 |
| TASK-044 | +21,213 | -7,177 |
| TASK-042 | +14,277 | -4,997 |
| TASK-041 | +14,237 | -22,909 |
| TASK-046 | +11,496 | -2,512 |
| TASK-010 | +10,882 | -9,572 |
| TASK-014 | +4,775 | -12,372 |
| TASK-009 | +4,474 | -32,180 |
| TASK-008 | +2,877 | -6,490 |
| TASK-001 | +1,640 | +35,687 |
| TASK-002 | +1,387 | -6,179 |
| TASK-012 | -595 | -4,357 |
| TASK-011 | -597 | +3,682 |
| TASK-013 | -597 | +3,942 |
| TASK-004 | -738 | +35,829 |
| TASK-007 | -911 | +3,351 |
| TASK-005 | -1,483 | +5,504 |
| TASK-003 | -1,509 | +28,378 |
| TASK-045 | -2,145 | +15,157 |
| TASK-006 | -2,776 | +24,660 |


## 4. Tâches où Token Savior perd

- **TASK-001** — active 9,080 → 44,767 | score 2→2
- **TASK-003** — active 17,037 → 45,415 | score 1→1
- **TASK-004** — active 9,427 → 45,256 | score 1→1
- **TASK-005** — active 9,331 → 14,835 | score 1→0
- **TASK-006** — active 21,869 → 46,529 | score 0→0
- **TASK-007** — active 9,136 → 12,487 | score 2→2
- **TASK-011** — active 9,220 → 12,902 | score 1→2
- **TASK-013** — active 9,192 → 13,134 | score 1→2
- **TASK-014** — active 27,232 → 14,860 | score 2→0
- **TASK-015** — active 9,906 → 12,698 | score 0→0
- **TASK-043** — active 19,531 → 26,573 | score 1→2
- **TASK-045** — active 8,497 → 23,654 | score 0→2

## 5. Tâches impossibles sans Token Savior

- **TASK-045** — score A=0, score B=2/2

## 6. Distribution des tool calls

**Run A (plain)** — top 5 :
- `Read` : 29
- `Grep` : 27
- `Glob` : 6
- `Agent` : 3
- `Bash` : 3

**Run B (token-savior)** — top 5 (TS/total = 0/409 = 0%) :
- `mcp__token-savior-recall__switch_project` : 60
- `mcp__token-savior-recall__get_function_source` : 60
- `mcp__token-savior-recall__search_codebase` : 50
- `mcp__token-savior-recall__get_structure_summary` : 38
- `mcp__token-savior-recall__list_files` : 32

## 7. Rapidité

- **Wall time moyen / tâche** : A=29.6s · B=28.5s (-4%)
- **Wall time total (14 tâches)** : A=622.6s · B=597.8s (-4%)

### Par catégorie

| Catégorie | N | Wall A moy | Wall B moy | Δ | Wall A total | Wall B total |
|---|---:|---:|---:|---:|---:|---:|
| call_chain | 3 | 13.4s | 44.9s | +236% | 40.1s | 134.8s |
| dépendants | 4 | 11.1s | 18.7s | +68% | 44.5s | 74.7s |
| heavy_read | 6 | 51.8s | 33.9s | -35% | 310.9s | 203.3s |
| impact | 2 | 69.0s | 29.5s | -57% | 137.9s | 58.9s |
| localisation | 6 | 14.9s | 21.0s | +41% | 89.1s | 126.0s |

### Tâches où TS est significativement plus rapide (>20%)

- **TASK-015** — 116.3s → 27.3s (-77%)
- **TASK-043** — 159.2s → 48.0s (-70%)
- **TASK-044** — 55.7s → 33.4s (-40%)

### Tâches où TS est significativement plus lent (>20%)

- **TASK-011** — 13.8s → 85.2s (+519%)
- **TASK-012** — 13.6s → 26.1s (+92%)
- **TASK-009** — 11.2s → 21.3s (+91%)
- **TASK-013** — 12.8s → 23.5s (+84%)
- **TASK-008** — 8.9s → 16.0s (+80%)
- **TASK-006** — 13.3s → 22.4s (+69%)
- **TASK-001** — 9.4s → 15.7s (+67%)
- **TASK-007** — 10.9s → 17.4s (+60%)
- **TASK-010** — 13.6s → 19.9s (+47%)
- **TASK-014** — 21.6s → 31.6s (+47%)
- **TASK-003** — 13.7s → 19.6s (+43%)
- **TASK-002** — 11.4s → 16.1s (+41%)
- **TASK-041** — 26.0s → 35.4s (+36%)
- **TASK-046** — 28.7s → 38.8s (+35%)
- **TASK-005** — 28.1s → 37.1s (+32%)
- **TASK-045** — 17.3s → 22.7s (+32%)


## 8. Données brutes

Voir [`results/raw/`](./raw/) pour les JSON par run.
