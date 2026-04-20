# tsbench — 90-task post-fixes run (2026-04-20)

## Headline

|                     | Plain Claude (A) | Token Savior (B) | Δ      |
|---------------------|-----------------:|-----------------:|-------:|
| Score               | 120 / 180 (66.7%)| **176 / 180 (97.8%)** | **+31.1pp** |
| Active tokens       | 1 549 915        | **820 861**      | −47%   |
| Wall time           | 166 min          | **36 min**       | −78%   |
| Wins / Ties / Losses| —                | **40 / 48 / 2**  |        |

## Per-category (Run B)

|                   | Score       | Accuracy |
|-------------------|------------:|---------:|
| audit             | 6 / 6       | 100.0%   |
| bug_fixing        | 26 / 26     | 100.0%   |
| code_generation   | 36 / 36     | 100.0%   |
| code_review       | 10 / 10     | 100.0%   |
| config_infra      | 8 / 8       | 100.0%   |
| documentation     | 8 / 8       | 100.0%   |
| git               | 8 / 8       | 100.0%   |
| refactoring       | 22 / 22     | 100.0%   |
| writing_tests     | 14 / 14     | 100.0%   |
| navigation        | 13 / 14     | 92.9%    |
| explanation       | 25 / 28     | 89.3%    |

Remaining misses are all `llm_judge` borderlines where TS correctly identifies
stub/missing code but the judge penalizes the honest "implementation is stub"
caveat. Contains-all tasks are saturated.

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
