# tsbench — RESULTS

_Generated 2026-04-15T09:09:25.832105+00:00_

## 1. Résumé exécutif

_Métrique principale : `active_tokens` = input + output + cache_creation (cache_read exclu — contexte réutilisé, proxy du coût quota abonnement)._

- **Tâches appariées** : 21
- **Réduction active_tokens A→B** : -3.8% (379,884 → 394,147)
- **Turns cumulés** : A=102 · B=182
- **Score global A** : 29/42 (69%)
- **Score global B** : 31/42 (74%)
- **Token Savior** : gagne 3, ex æquo 17, perd 1

## 2. Tableau principal

| Task | Catégorie | Active A | Active B | ΔActive | Chars A | Chars B | ΔChars | Score A | Score B |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| TASK-001 | localisation | 9080 | 44204 | -387% | 1,761 | 121 | +93% | 2/2 | 2/2 |
| TASK-002 | localisation | 17679 | 5022 | +72% | 1,737 | 410 | +76% | 2/2 | 2/2 |
| TASK-003 | localisation | 17037 | 11671 | +31% | 280 | 1,789 | -539% | 1/2 | 1/2 |
| TASK-004 | localisation | 9427 | 16821 | -78% | 558 | 16,510 | -2859% | 1/2 | 1/2 |
| TASK-005 | localisation | 9331 | 48216 | -417% | 720 | 4,675 | -549% | 1/2 | 0/2 |
| TASK-006 | localisation | 21869 | 45528 | -108% | 986 | 2,588 | -162% | 0/2 | 0/2 |
| TASK-007 | dépendants | 9136 | 12700 | -39% | 1,761 | 2,733 | -55% | 2/2 | 2/2 |
| TASK-008 | dépendants | 18033 | 13098 | +27% | 3,227 | 4,827 | -50% | 2/2 | 2/2 |
| TASK-009 | dépendants | 44160 | 11931 | +73% | 5,231 | 757 | +86% | 2/2 | 2/2 |
| TASK-010 | dépendants | 22492 | 17306 | +23% | 12,668 | 1,845 | +85% | 2/2 | 2/2 |
| TASK-011 | call_chain | 9220 | 12491 | -35% | 1,364 | 545 | +60% | 1/2 | 2/2 |
| TASK-012 | call_chain | 21860 | 12439 | +43% | 1,327 | 531 | +60% | 1/2 | 2/2 |
| TASK-013 | call_chain | 9192 | 12414 | -35% | 1,364 | 545 | +60% | 1/2 | 2/2 |
| TASK-014 | impact | 27232 | 16529 | +39% | 12,668 | 5,788 | +54% | 2/2 | 2/2 |
| TASK-015 | impact | 9906 | 15865 | -60% | — | 7,542 | — | 0/2 | 0/2 |
| TASK-016 | impact | — | 11457 | — | — | 254 | — | — | 0/2 |
| TASK-017 | edit | — | 15366 | — | — | 1,255 | — | — | 1/2 |
| TASK-018 | edit | — | 15430 | — | — | 2,445 | — | — | 1/2 |
| TASK-019 | edit | — | 19487 | — | — | 12,122 | — | — | 0/2 |
| TASK-020 | edit | — | 18831 | — | — | 6,269 | — | — | 1/2 |
| TASK-021 | review | — | 13534 | — | — | 5,597 | — | — | 0/2 |
| TASK-022 | review | — | 20347 | — | — | 33,587 | — | — | 0/2 |
| TASK-023 | review | — | 5753 | — | — | 952 | — | — | 2/2 |
| TASK-024 | audit | — | 9164 | — | — | 7,866 | — | — | 0/2 |
| TASK-025 | audit | — | 44629 | — | — | 382 | — | — | 0/2 |
| TASK-026 | audit | — | 24834 | — | — | 6,140 | — | — | 0/2 |
| TASK-027 | config | — | 10467 | — | — | 11,371 | — | — | 0/2 |
| TASK-028 | config | — | 7964 | — | — | 7,881 | — | — | 0/2 |
| TASK-029 | config | — | 6586 | — | — | 3,796 | — | — | 0/2 |
| TASK-030 | infra | — | 5273 | — | — | 307 | — | — | 0/2 |
| TASK-031 | infra | — | 17398 | — | — | 26,482 | — | — | 0/2 |
| TASK-032 | testing | — | 5372 | — | — | 501 | — | — | 0/2 |
| TASK-033 | testing | — | 14136 | — | — | 3,494 | — | — | 0/2 |
| TASK-034 | debug | — | 9656 | — | — | 7,113 | — | — | 2/2 |
| TASK-035 | debug | — | 9367 | — | — | 11,621 | — | — | 2/2 |
| TASK-036 | debug | — | 12159 | — | — | 8,182 | — | — | 0/2 |
| TASK-037 | onboarding | — | 4374 | — | — | 2,800 | — | — | 0/2 |
| TASK-038 | onboarding | — | 7681 | — | — | 2,950 | — | — | 0/2 |
| TASK-039 | cross-language | — | 6321 | — | — | 829 | — | — | 0/2 |
| TASK-040 | cross-language | — | 9094 | — | — | 6,232 | — | — | 0/2 |
| TASK-041 | heavy_read | 33525 | 12863 | +62% | 23,633 | 10,424 | +56% | 2/2 | 2/2 |
| TASK-042 | heavy_read | 18667 | 15374 | +18% | 18,895 | 5,653 | +70% | 2/2 | 2/2 |
| TASK-043 | heavy_read | 19531 | 25908 | -33% | 196,882 | 16,216 | +92% | 1/2 | 1/2 |
| TASK-044 | heavy_read | 23485 | 14269 | +39% | 30,789 | 2,422 | +92% | 2/2 | 2/2 |
| TASK-045 | heavy_read | 8497 | 12034 | -42% | 14 | 476 | -3300% | 0/2 | 0/2 |
| TASK-046 | heavy_read | 20525 | 17464 | +15% | 20,258 | 8,303 | +59% | 2/2 | 2/2 |
| TASK-047 | navigation | — | 11513 | — | — | 180 | — | — | 2/2 |
| TASK-048 | navigation | — | 11813 | — | — | 561 | — | — | 2/2 |
| TASK-049 | call_chain | — | 11628 | — | — | 301 | — | — | 2/2 |
| TASK-050 | navigation | — | 14162 | — | — | 2,782 | — | — | 1/2 |
| TASK-051 | navigation | — | 13654 | — | — | 4,989 | — | — | 2/2 |
| TASK-052 | audit | — | 20018 | — | — | 3,709 | — | — | 2/2 |
| TASK-053 | audit | — | 18281 | — | — | 7,927 | — | — | 1/2 |
| TASK-054 | edit | — | 45265 | — | — | 923 | — | — | 2/2 |
| TASK-055 | edit | — | 44362 | — | — | 353 | — | — | 2/2 |
| TASK-056 | edit | — | 49424 | — | — | 2,588 | — | — | 2/2 |
| TASK-057 | testing | — | 11860 | — | — | 242 | — | — | 2/2 |
| TASK-058 | audit | — | 18525 | — | — | 9,710 | — | — | 2/2 |
| TASK-059 | git | — | 12383 | — | — | 1,612 | — | — | 2/2 |
| TASK-060 | git | — | 13740 | — | — | 4,180 | — | — | 2/2 |

## 3. Moyennes par catégorie

| Catégorie | N | Active A moy | Active B moy | Réduction | Turns A moy | Turns B moy | Score A moy | Score B moy |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| call_chain | 3 | 13,424 | 12,448 | +7% | 4.3 | 8.0 | 1.00 | 2.00 |
| dépendants | 4 | 23,455 | 13,759 | +41% | 2.0 | 5.5 | 2.00 | 2.00 |
| heavy_read | 6 | 20,705 | 16,319 | +21% | 6.8 | 12.8 | 1.50 | 1.50 |
| impact | 2 | 18,569 | 16,197 | +13% | 9.0 | 13.0 | 1.00 | 1.00 |
| localisation | 6 | 14,070 | 28,577 | -103% | 3.7 | 5.5 | 1.17 | 1.00 |

## 3bis. Analyse chars_injected (ce que TS prétend économiser)

- **Pairs mesurés** : 20
- **Chars injectés cumulés** : A=336,123 · B=87,158 · Δ=+74%
- **TS gagne sur chars** : 13/20
- **TS perd sur chars** : 7/20
- **Ex æquo** : 0/20

### Tâches où TS gagne sur chars_injected

- **TASK-043** — chars 196,882→16,216 (-92%) | active 19,531→25,908 (+33%)
- **TASK-044** — chars 30,789→2,422 (-92%) | active 23,485→14,269 (-39%)
- **TASK-042** — chars 18,895→5,653 (-70%) | active 18,667→15,374 (-18%)
- **TASK-041** — chars 23,633→10,424 (-56%) | active 33,525→12,863 (-62%)
- **TASK-046** — chars 20,258→8,303 (-59%) | active 20,525→17,464 (-15%)
- **TASK-010** — chars 12,668→1,845 (-85%) | active 22,492→17,306 (-23%)
- **TASK-014** — chars 12,668→5,788 (-54%) | active 27,232→16,529 (-39%)
- **TASK-009** — chars 5,231→757 (-86%) | active 44,160→11,931 (-73%)
- **TASK-001** — chars 1,761→121 (-93%) | active 9,080→44,204 (+387%)
- **TASK-002** — chars 1,737→410 (-76%) | active 17,679→5,022 (-72%)
- **TASK-011** — chars 1,364→545 (-60%) | active 9,220→12,491 (+35%)
- **TASK-013** — chars 1,364→545 (-60%) | active 9,192→12,414 (+35%)
- **TASK-012** — chars 1,327→531 (-60%) | active 21,860→12,439 (-43%)

### Tâches où TS perd sur chars_injected

- **TASK-004** — chars 558→16,510 (+2859%) | active 9,427→16,821 (+78%)
- **TASK-005** — chars 720→4,675 (+549%) | active 9,331→48,216 (+417%)
- **TASK-006** — chars 986→2,588 (+162%) | active 21,869→45,528 (+108%)
- **TASK-008** — chars 3,227→4,827 (+50%) | active 18,033→13,098 (-27%)
- **TASK-003** — chars 280→1,789 (+539%) | active 17,037→11,671 (-31%)
- **TASK-007** — chars 1,761→2,733 (+55%) | active 9,136→12,700 (+39%)
- **TASK-045** — chars 14→476 (+3300%) | active 8,497→12,034 (+42%)

### Break-even analysis

_Coût fixe B = active_tokens B − chars_injected B (baseline TS : system prompt, schémas ToolSearch). Gain chars = chars_A − chars_B. TS rentable sur active_tokens si : (active_A − active_B) ≥ 0, i.e. le gain chars_injected doit couvrir le surcoût baseline._

- **Surcoût moyen active_tokens B − A** : +415 tokens / tâche
- **Cas où B ≤ A sur active** : 11/20

| Task | Gain chars (A−B) | Surcoût active (B−A) |
|---|---:|---:|
| TASK-043 | +180,666 | +6,377 |
| TASK-044 | +28,367 | -9,216 |
| TASK-042 | +13,242 | -3,293 |
| TASK-041 | +13,209 | -20,662 |
| TASK-046 | +11,955 | -3,061 |
| TASK-010 | +10,823 | -5,186 |
| TASK-014 | +6,880 | -10,703 |
| TASK-009 | +4,474 | -32,229 |
| TASK-001 | +1,640 | +35,124 |
| TASK-002 | +1,327 | -12,657 |
| TASK-011 | +819 | +3,271 |
| TASK-013 | +819 | +3,222 |
| TASK-012 | +796 | -9,421 |
| TASK-045 | -462 | +3,537 |
| TASK-007 | -972 | +3,564 |
| TASK-003 | -1,509 | -5,366 |
| TASK-008 | -1,600 | -4,935 |
| TASK-006 | -1,602 | +23,659 |
| TASK-005 | -3,955 | +38,885 |
| TASK-004 | -15,952 | +7,394 |


## 4. Tâches où Token Savior perd

- **TASK-001** — active 9,080 → 44,204 | score 2→2
- **TASK-004** — active 9,427 → 16,821 | score 1→1
- **TASK-005** — active 9,331 → 48,216 | score 1→0
- **TASK-006** — active 21,869 → 45,528 | score 0→0
- **TASK-007** — active 9,136 → 12,700 | score 2→2
- **TASK-011** — active 9,220 → 12,491 | score 1→2
- **TASK-013** — active 9,192 → 12,414 | score 1→2
- **TASK-015** — active 9,906 → 15,865 | score 0→0
- **TASK-043** — active 19,531 → 25,908 | score 1→1
- **TASK-045** — active 8,497 → 12,034 | score 0→0

## 5. Tâches impossibles sans Token Savior

_Aucune._

## 6. Distribution des tool calls

**Run A (plain)** — top 5 :
- `Read` : 29
- `Grep` : 27
- `Glob` : 6
- `Agent` : 3
- `Bash` : 3

**Run B (token-savior)** — top 5 (TS/total = 0/468 = 0%) :
- `mcp__token-savior-recall__get_function_source` : 107
- `mcp__token-savior-recall__switch_project` : 60
- `mcp__token-savior-recall__search_codebase` : 47
- `mcp__token-savior-recall__list_files` : 40
- `mcp__token-savior-recall__get_structure_summary` : 37

## 7. Rapidité

- **Wall time moyen / tâche** : A=29.6s · B=28.5s (-4%)
- **Wall time total (14 tâches)** : A=622.6s · B=599.3s (-4%)

### Par catégorie

| Catégorie | N | Wall A moy | Wall B moy | Δ | Wall A total | Wall B total |
|---|---:|---:|---:|---:|---:|---:|
| call_chain | 3 | 13.4s | 30.8s | +130% | 40.1s | 92.3s |
| dépendants | 4 | 11.1s | 19.8s | +78% | 44.5s | 79.1s |
| heavy_read | 6 | 51.8s | 37.3s | -28% | 310.9s | 224.1s |
| impact | 2 | 69.0s | 40.0s | -42% | 137.9s | 80.1s |
| localisation | 6 | 14.9s | 20.6s | +39% | 89.1s | 123.8s |

### Tâches où TS est significativement plus rapide (>20%)

- **TASK-043** — 159.2s → 34.5s (-78%)
- **TASK-015** — 116.3s → 39.5s (-66%)

### Tâches où TS est significativement plus lent (>20%)

- **TASK-013** — 12.8s → 31.8s (+149%)
- **TASK-012** — 13.6s → 31.6s (+132%)
- **TASK-011** — 13.8s → 28.9s (+110%)
- **TASK-007** — 10.9s → 21.2s (+95%)
- **TASK-014** — 21.6s → 40.5s (+88%)
- **TASK-008** — 8.9s → 15.9s (+80%)
- **TASK-041** — 26.0s → 45.5s (+75%)
- **TASK-010** — 13.6s → 23.4s (+72%)
- **TASK-002** — 11.4s → 19.6s (+72%)
- **TASK-009** — 11.2s → 18.5s (+65%)
- **TASK-001** — 9.4s → 15.4s (+64%)
- **TASK-046** — 28.7s → 43.0s (+49%)
- **TASK-004** — 13.2s → 19.4s (+47%)
- **TASK-045** — 17.3s → 22.7s (+32%)
- **TASK-005** — 28.1s → 36.7s (+31%)
- **TASK-006** — 13.3s → 17.1s (+29%)
- **TASK-042** — 24.0s → 30.5s (+27%)


## 8. Données brutes

Voir [`results/raw/`](./raw/) pour les JSON par run.
