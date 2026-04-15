# tsbench — RESULTS

_Generated 2026-04-15T07:46:47.891139+00:00_

## 1. Résumé exécutif

_Métrique principale : `active_tokens` = input + output + cache_creation (cache_read exclu — contexte réutilisé, proxy du coût quota abonnement)._

- **Tâches appariées** : 20
- **Réduction active_tokens A→B** : -8.5% (369,978 → 401,521)
- **Turns cumulés** : A=88 · B=182
- **Score global A** : 29/40 (72%)
- **Score global B** : 35/40 (88%)
- **Token Savior** : gagne 5, ex æquo 15, perd 0

## 2. Tableau principal

| Task | Catégorie | Active A | Active B | ΔActive | Chars A | Chars B | ΔChars | Score A | Score B |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| TASK-001 | localisation | 9080 | 21036 | -132% | 1,761 | 337 | +81% | 2/2 | 2/2 |
| TASK-002 | localisation | 17679 | 10822 | +39% | 1,737 | 540 | +69% | 2/2 | 2/2 |
| TASK-003 | localisation | 17037 | 11629 | +32% | 280 | 2,113 | -655% | 1/2 | 1/2 |
| TASK-004 | localisation | 9427 | 13318 | -41% | 558 | 4,508 | -708% | 1/2 | 1/2 |
| TASK-005 | localisation | 9331 | 13449 | -44% | 720 | 2,951 | -310% | 1/2 | 1/2 |
| TASK-006 | localisation | 21869 | 12443 | +43% | 986 | 1,862 | -89% | 0/2 | 0/2 |
| TASK-007 | dépendants | 9136 | 11405 | -25% | 1,761 | 548 | +69% | 2/2 | 2/2 |
| TASK-008 | dépendants | 18033 | 23308 | -29% | 3,227 | 1,619 | +50% | 2/2 | 2/2 |
| TASK-009 | dépendants | 44160 | 11429 | +74% | 5,231 | 1,122 | +79% | 2/2 | 2/2 |
| TASK-010 | dépendants | 22492 | 13146 | +42% | 12,668 | 2,295 | +82% | 2/2 | 2/2 |
| TASK-011 | call_chain | 9220 | 10016 | -9% | 1,364 | 539 | +60% | 1/2 | 2/2 |
| TASK-012 | call_chain | 21860 | 5635 | +74% | 1,327 | 528 | +60% | 1/2 | 2/2 |
| TASK-013 | call_chain | 9192 | 44696 | -386% | 1,364 | 539 | +60% | 1/2 | 2/2 |
| TASK-014 | impact | 27232 | 15446 | +43% | 12,668 | 2,785 | +78% | 2/2 | 2/2 |
| TASK-015 | impact | 9906 | — | — | — | — | — | 0/2 | — |
| TASK-041 | heavy_read | 33525 | 50061 | -49% | 23,633 | 5,990 | +75% | 2/2 | 2/2 |
| TASK-042 | heavy_read | 18667 | 8693 | +53% | 18,895 | 5,031 | +73% | 2/2 | 2/2 |
| TASK-043 | heavy_read | 19531 | 19750 | -1% | 196,882 | 16,248 | +92% | 1/2 | 2/2 |
| TASK-044 | heavy_read | 23485 | 9805 | +58% | 30,789 | 2,660 | +91% | 2/2 | 2/2 |
| TASK-045 | heavy_read | 8497 | 45092 | -431% | 14 | 1,602 | -11343% | 0/2 | 2/2 |
| TASK-046 | heavy_read | 20525 | 50342 | -145% | 20,258 | 7,892 | +61% | 2/2 | 2/2 |
| TASK-047 | navigation | — | 4865 | — | — | 212 | — | — | 2/2 |
| TASK-048 | navigation | — | 5207 | — | — | 559 | — | — | 2/2 |
| TASK-049 | call_chain | — | 4927 | — | — | 301 | — | — | 2/2 |
| TASK-050 | navigation | — | 6953 | — | — | 2,741 | — | — | 1/2 |
| TASK-051 | navigation | — | 7092 | — | — | 5,068 | — | — | 2/2 |
| TASK-052 | audit | — | 17845 | — | — | 16,056 | — | — | 2/2 |
| TASK-053 | audit | — | 7575 | — | — | 6,318 | — | — | 2/2 |
| TASK-054 | edit | — | 8675 | — | — | 2,258 | — | — | 2/2 |
| TASK-055 | edit | — | 44193 | — | — | 346 | — | — | 2/2 |
| TASK-056 | edit | — | 46503 | — | — | 1,524 | — | — | 2/2 |
| TASK-057 | testing | — | 11474 | — | — | 274 | — | — | 2/2 |
| TASK-058 | audit | — | 6041 | — | — | 1,680 | — | — | 2/2 |
| TASK-059 | git | — | 9255 | — | — | 776 | — | — | 2/2 |
| TASK-060 | git | — | 15555 | — | — | 10,676 | — | — | 2/2 |

## 3. Moyennes par catégorie

| Catégorie | N | Active A moy | Active B moy | Réduction | Turns A moy | Turns B moy | Score A moy | Score B moy |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| call_chain | 3 | 13,424 | 20,116 | -50% | 4.3 | 7.0 | 1.00 | 2.00 |
| dépendants | 4 | 23,455 | 14,822 | +37% | 2.0 | 6.5 | 2.00 | 2.00 |
| heavy_read | 6 | 20,705 | 30,624 | -48% | 6.8 | 13.7 | 1.50 | 2.00 |
| impact | 1 | 27,232 | 15,446 | +43% | 4.0 | 11.0 | 2.00 | 2.00 |
| localisation | 6 | 14,070 | 13,783 | +2% | 3.7 | 7.0 | 1.17 | 1.17 |

## 3bis. Analyse chars_injected (ce que TS prétend économiser)

- **Pairs mesurés** : 20
- **Chars injectés cumulés** : A=336,123 · B=61,709 · Δ=+82%
- **TS gagne sur chars** : 15/20
- **TS perd sur chars** : 5/20
- **Ex æquo** : 0/20

### Tâches où TS gagne sur chars_injected

- **TASK-043** — chars 196,882→16,248 (-92%) | active 19,531→19,750 (+1%)
- **TASK-044** — chars 30,789→2,660 (-91%) | active 23,485→9,805 (-58%)
- **TASK-041** — chars 23,633→5,990 (-75%) | active 33,525→50,061 (+49%)
- **TASK-042** — chars 18,895→5,031 (-73%) | active 18,667→8,693 (-53%)
- **TASK-046** — chars 20,258→7,892 (-61%) | active 20,525→50,342 (+145%)
- **TASK-010** — chars 12,668→2,295 (-82%) | active 22,492→13,146 (-42%)
- **TASK-014** — chars 12,668→2,785 (-78%) | active 27,232→15,446 (-43%)
- **TASK-009** — chars 5,231→1,122 (-79%) | active 44,160→11,429 (-74%)
- **TASK-008** — chars 3,227→1,619 (-50%) | active 18,033→23,308 (+29%)
- **TASK-001** — chars 1,761→337 (-81%) | active 9,080→21,036 (+132%)
- **TASK-007** — chars 1,761→548 (-69%) | active 9,136→11,405 (+25%)
- **TASK-002** — chars 1,737→540 (-69%) | active 17,679→10,822 (-39%)
- **TASK-011** — chars 1,364→539 (-60%) | active 9,220→10,016 (+9%)
- **TASK-013** — chars 1,364→539 (-60%) | active 9,192→44,696 (+386%)
- **TASK-012** — chars 1,327→528 (-60%) | active 21,860→5,635 (-74%)

### Tâches où TS perd sur chars_injected

- **TASK-004** — chars 558→4,508 (+708%) | active 9,427→13,318 (+41%)
- **TASK-005** — chars 720→2,951 (+310%) | active 9,331→13,449 (+44%)
- **TASK-003** — chars 280→2,113 (+655%) | active 17,037→11,629 (-32%)
- **TASK-045** — chars 14→1,602 (+11343%) | active 8,497→45,092 (+431%)
- **TASK-006** — chars 986→1,862 (+89%) | active 21,869→12,443 (-43%)

### Break-even analysis

_Coût fixe B = active_tokens B − chars_injected B (baseline TS : system prompt, schémas ToolSearch). Gain chars = chars_A − chars_B. TS rentable sur active_tokens si : (active_A − active_B) ≥ 0, i.e. le gain chars_injected doit couvrir le surcoût baseline._

- **Surcoût moyen active_tokens B − A** : +1,577 tokens / tâche
- **Cas où B ≤ A sur active** : 9/20

| Task | Gain chars (A−B) | Surcoût active (B−A) |
|---|---:|---:|
| TASK-043 | +180,634 | +219 |
| TASK-044 | +28,129 | -13,680 |
| TASK-041 | +17,643 | +16,536 |
| TASK-042 | +13,864 | -9,974 |
| TASK-046 | +12,366 | +29,817 |
| TASK-010 | +10,373 | -9,346 |
| TASK-014 | +9,883 | -11,786 |
| TASK-009 | +4,109 | -32,731 |
| TASK-008 | +1,608 | +5,275 |
| TASK-001 | +1,424 | +11,956 |
| TASK-007 | +1,213 | +2,269 |
| TASK-002 | +1,197 | -6,857 |
| TASK-011 | +825 | +796 |
| TASK-013 | +825 | +35,504 |
| TASK-012 | +799 | -16,225 |
| TASK-006 | -876 | -9,426 |
| TASK-045 | -1,588 | +36,595 |
| TASK-003 | -1,833 | -5,408 |
| TASK-005 | -2,231 | +4,118 |
| TASK-004 | -3,950 | +3,891 |


## 4. Tâches où Token Savior perd

- **TASK-001** — active 9,080 → 21,036 | score 2→2
- **TASK-004** — active 9,427 → 13,318 | score 1→1
- **TASK-005** — active 9,331 → 13,449 | score 1→1
- **TASK-007** — active 9,136 → 11,405 | score 2→2
- **TASK-008** — active 18,033 → 23,308 | score 2→2
- **TASK-011** — active 9,220 → 10,016 | score 1→2
- **TASK-013** — active 9,192 → 44,696 | score 1→2
- **TASK-041** — active 33,525 → 50,061 | score 2→2
- **TASK-043** — active 19,531 → 19,750 | score 1→2
- **TASK-045** — active 8,497 → 45,092 | score 0→2
- **TASK-046** — active 20,525 → 50,342 | score 2→2

## 5. Tâches impossibles sans Token Savior

- **TASK-045** — score A=0, score B=2/2

## 6. Distribution des tool calls

**Run A (plain)** — top 5 :
- `Read` : 29
- `Grep` : 27
- `Glob` : 6
- `Agent` : 3
- `Bash` : 3

**Run B (token-savior)** — top 5 (TS/total = 51/192 = 27%) :
- `mcp__token-savior-recall__get_function_source` : 29
- `mcp__token-savior-recall__switch_project` : 20
- `ToolSearch` : 17
- `mcp__token-savior-recall__memory_search` : 15
- `mcp__token-savior-recall__get_functions` : 15

## 7. Rapidité

- **Wall time moyen / tâche** : A=25.3s · B=32.0s (+26%)
- **Wall time total (14 tâches)** : A=506.3s · B=639.2s (+26%)

### Par catégorie

| Catégorie | N | Wall A moy | Wall B moy | Δ | Wall A total | Wall B total |
|---|---:|---:|---:|---:|---:|---:|
| call_chain | 3 | 13.4s | 37.1s | +177% | 40.1s | 111.3s |
| dépendants | 4 | 11.1s | 24.6s | +121% | 44.5s | 98.4s |
| heavy_read | 6 | 51.8s | 40.5s | -22% | 310.9s | 243.2s |
| impact | 1 | 21.6s | 41.2s | +91% | 21.6s | 41.2s |
| localisation | 6 | 14.9s | 24.2s | +63% | 89.1s | 145.2s |

### Tâches où TS est significativement plus rapide (>20%)

- **TASK-043** — 159.2s → 36.2s (-77%)
- **TASK-044** — 55.7s → 42.8s (-23%)

### Tâches où TS est significativement plus lent (>20%)

- **TASK-013** — 12.8s → 50.6s (+296%)
- **TASK-008** — 8.9s → 28.0s (+216%)
- **TASK-004** — 13.2s → 32.5s (+147%)
- **TASK-011** — 13.8s → 32.7s (+138%)
- **TASK-007** — 10.9s → 24.5s (+126%)
- **TASK-006** — 13.3s → 29.0s (+118%)
- **TASK-012** — 13.6s → 28.0s (+106%)
- **TASK-041** — 26.0s → 51.2s (+97%)
- **TASK-014** — 21.6s → 41.2s (+91%)
- **TASK-009** — 11.2s → 21.3s (+90%)
- **TASK-010** — 13.6s → 24.5s (+80%)
- **TASK-042** — 24.0s → 40.9s (+71%)
- **TASK-045** — 17.3s → 28.3s (+64%)
- **TASK-002** — 11.4s → 17.6s (+54%)
- **TASK-046** — 28.7s → 43.8s (+52%)
- **TASK-003** — 13.7s → 20.0s (+46%)
- **TASK-001** — 9.4s → 13.2s (+40%)


## 8. Données brutes

Voir [`results/raw/`](./raw/) pour les JSON par run.
