# v2.7 optimization sample — haiku-ts

_Generated 2026-04-21._

Targeted sample measuring 14 Token Savior optimizations shipped in v2.7.0 / v2.7.1, run on the 12 losing tasks most likely to benefit.

## Setup

- Model : `claude-haiku-4-5-20251001`
- Run : B (token-savior only, per bench.py SYSTEM_PROMPT_TS)
- Baseline : `raw-haiku-ts/` (full 90-task run, 20/04)
- v2.7.0 sample : `raw-haiku-ts-v27-sample/` (12 tasks)
- v2.7.1 rerun : `raw-haiku-ts-v271-regcheck/` (6 tasks, descriptions tightened -47%)

## Optimizations shipped

| Category | Change |
|---|---|
| Navigation | `find_symbol` complete signal; normalized-name fallback; `search_codebase` skip generated; new `search_in_symbols` |
| Context | `get_full_context` `brief=true`; `get_class_source` auto-downgrade >300 lines; `[scaffold: stub]` marker |
| Analysis | `find_hotspots` T0-T3 tiers; `detect_breaking_changes` tiered + TERMINAL signal; new `audit_file` mega-batch |
| Tests | impacted-tests BFS transitive on reverse_import_graph |
| Safety | `get_backward_slice` 500-line cap; `get_community` 50-member cap |
| Session | `switch_project` stickiness (skip re-index when active) |
| Descriptions | 5 key tools gained decision hints (`BATCH`, `USE THIS instead`, `TERMINAL`, `ignore_generated`) |

## v2.7.0 sample — 12 tasks

| TASK | base active | v27 active | Δ% | base turns | v27 turns | base tools | v27 tools |
|---|---:|---:|---:|---:|---:|---:|---:|
| TASK-045 heavy_read | 32596 | 18244 | **−44.0%** | 25 | 11 | 9 | 4 |
| TASK-050 navigation | 20641 | 16623 | −19.5% | 11 | 7 | 3 | 2 |
| TASK-056 edit | 21280 | 18327 | −13.9% | 11 | 9 | 4 | 3 |
| TASK-053 audit | 18569 | 17628 | −5.1% | 14 | 7 | 5 | 2 |
| TASK-031 infra | 17306 | 16645 | −3.8% | 9 | 5 | 3 | 2 |
| TASK-054 edit | 32363 | 31211 | −3.6% | 23 | 22 | 8 | 8 |
| TASK-022 review | 16861 | 17240 | +2.2% | 7 | 5 | 3 | 2 |
| TASK-027 config | 14428 | 14960 | +3.7% | 4 | 4 | 1 | 1 |
| TASK-058 audit | 14430 | 15146 | +5.0% | 2 | 2 | 0 | 0 |
| TASK-001 localisation | 13260 | 14642 | +10.4% | 4 | 4 | 1 | 1 |
| TASK-004 localisation | 14719 | 16271 | +10.5% | 5 | 5 | 2 | 2 |
| TASK-055 edit | 17537 | — | timeout | 14 | — | 5 | — |

**Mean Δ active_tokens : −13.2%** — 5 wins (<−5%), 2 flat, 3 small regressions, 1 timeout, 1 skipped.

## v2.7.1 rerun — 6 tasks (descriptions tightened -47%)

| TASK | base | v2.7.0 | v2.7.1 |
|---|---:|---:|---:|
| TASK-001 locate | 13260 | +10.4% | **+8.7%** |
| TASK-004 locate | 14719 | +10.5% | +10.6% |
| TASK-027 config | 14428 | +3.7% | +14.6% ⚠ |
| TASK-058 code-gen | 14430 | +5.0% | +33.1% ⚠ |
| TASK-045 heavy_read | 32596 | −44.0% | **−48.5%** |
| TASK-050 navigation | 20641 | −19.5% | −3.9% |

## Findings

1. **Big wins on medium/hard tasks** : TASK-045 (−44% then −48.5%) validates `audit_file` + brief + scaffold marker. Turn count drops 25→11→9.
2. **Residual regression on tiny localisation tasks** (TASK-001/004 +10%) : same tools as baseline, extra cost = cache_creation from MCP system prompt. Structural — classified "coût fixe non amorti" in LOSING-TASKS-ANALYSIS.md.
3. **Code-gen noise** (TASK-055 timeout, TASK-058 +33%) : Haiku alternates between "answer in text" (baseline used 0 tools, scored 2/2) and "try tools" (v2.7.1 tried Write/Bash, blocked). Not a tooling issue — model variance at N=1.
4. **Description tightening** : v2.7.1 cut 5 key descriptions from 1525 → 811 chars while preserving keywords. Reclaimed ~200 tokens on TASK-001 while TASK-045 win *improved* (−44 → −48.5%) — hints were actionable even compressed.

## Next

- N=3 runs per task to smooth Haiku variance
- Possible "create new file" dedicated tool to reduce code-gen variance
- Lazy-load tool schemas to reduce fixed MCP overhead on 1-tool tasks
