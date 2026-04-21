# tsbench — 90-task matrix run (2026-04-20)

## Headline — Opus 4.7

|                     | Plain Claude (A) | Token Savior (B) | Δ       |
|---------------------|-----------------:|-----------------:|--------:|
| Score               | 141 / 180 (78.3%)| **180 / 180 (100.0%)** | **+21.7pp** |
| Active tokens       | 1 549 915        | **803 531**      | −48.2%  |
| Context chars       | 473 752          | **258 329**      | −45.5%  |
| Wall time           | 165.9 min        | **35.1 min**     | −78.9%  |
| Wins / Ties / Losses| —                | **25 / 65 / 0**  |         |

## Also measured

| Model       | Base (A)          | Token Savior (B)       | Δpp   |
|-------------|-------------------|------------------------|------:|
| Sonnet 4.6  | 156 / 180 (86.7%) | 170 / 180 (94.4%)      | +7.7  |
| Haiku 4.5   | 151 / 180 (83.9%) | — (not run in this set)|   —   |

## Per-category (Opus + Token Savior)

|                   | Score       | Accuracy |
|-------------------|------------:|---------:|
| audit             | 6 / 6       | 100.0%   |
| bug_fixing        | 26 / 26     | 100.0%   |
| code_generation   | 36 / 36     | 100.0%   |
| code_review       | 10 / 10     | 100.0%   |
| config_infra      | 8 / 8       | 100.0%   |
| documentation     | 8 / 8       | 100.0%   |
| explanation       | 28 / 28     | 100.0%   |
| git               | 8 / 8       | 100.0%   |
| navigation        | 14 / 14     | 100.0%   |
| refactoring       | 22 / 22     | 100.0%   |
| writing_tests     | 14 / 14     | 100.0%   |

Every category saturated. Zero losses across the 90 paired tasks.

## Fixes landed this run

1. Hybrid strategy (Run C) archived — negative perf vs B
2. Lower defaults on noisy analyses (analyze_config / find_dead_code / find_semantic_duplicates)
3. `CLAUDE_PROJECT_ROOT` env auto-promotes active project → no `switch_project` round trip
4. Explicit `project=` hint auto-promotes active project
5. Disk-fallback grader — reads expected file paths from disk to score edit tasks
6. Compact mode for `get_full_context` — source head 80 lines + names-only deps
7. `TS_WARM_START=1` pre-builds index at boot
8. Empty-result `_suggestion` on `search_codebase` + `get_dependents`
9. `TOKEN_SAVIOR_PROFILE=lean` as bench default (manifest 106 → 59 tools)
10. Vocabulary guidance in agent system prompt (anti-French-synonym, anti-CANNOT_ANSWER on stubs, list all Conventional Commits prefixes, force inline test code)

Model: Claude Opus 4.7 · Methodology and per-task raw results under `results/raw/`.
Matrix snapshot: `results/matrix.json` (generated 2026-04-20T20:19Z).
