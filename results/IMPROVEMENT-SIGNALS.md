# Token Savior — Improvement Signals (Run B)

_Analyzed 60 tasks, 408 TS tool calls._

## 1. Top 10 empty calls (`result_chars < 50`)

| # | Task | Tool | Args | Chars |
|---|------|------|------|-------|
| 1 | TASK-027 | `get_functions` | `{"file_path": "config/.env.example"}` | 2 |
| 2 | TASK-040 | `get_functions` | `{"file_path": "apps/api/config.py", "hints": false}` | 2 |
| 3 | TASK-018 | `list_files` | `{"pattern": "*schema.prisma*"}` | 2 |
| 4 | TASK-018 | `list_files` | `{"pattern": "*prisma*"}` | 2 |
| 5 | TASK-019 | `list_files` | `{"pattern": "apps/web/constants*"}` | 2 |
| 6 | TASK-019 | `list_files` | `{"pattern": "packages/*/constants*"}` | 2 |
| 7 | TASK-019 | `list_files` | `{"pattern": "packages/config*"}` | 2 |
| 8 | TASK-027 | `list_files` | `{"pattern": ".env.example"}` | 2 |
| 9 | TASK-030 | `list_files` | `{"pattern": "**/Docker*"}` | 2 |
| 10 | TASK-037 | `list_files` | `{"max_results": 10, "pattern": "results/*"}` | 2 |

## 2. Top 5 chaining sequences (A -> B -> C)

| # | Chain | Frequency |
|---|-------|-----------|
| 1 | `get_function_source` -> `get_function_source` -> `get_function_source` | 24 |
| 2 | `get_functions` -> `get_functions` -> `get_functions` | 11 |
| 3 | `search_codebase` -> `search_codebase` -> `search_codebase` | 10 |
| 4 | `get_full_context` -> `get_full_context` -> `get_full_context` | 9 |
| 5 | `get_community` -> `get_community` -> `get_community` | 8 |

**Top 5 pairs (A -> B):**

| # | Pair | Frequency |
|---|------|-----------|
| 1 | `get_function_source` -> `get_function_source` | 35 |
| 2 | `search_codebase` -> `search_codebase` | 19 |
| 3 | `get_full_context` -> `get_full_context` | 13 |
| 4 | `list_files` -> `list_files` | 13 |
| 5 | `get_structure_summary` -> `get_structure_summary` | 13 |

## 3. Top 5 slowest tools (median `time_ms`)

| # | Tool | Median ms | Peak ms | Calls |
|---|------|-----------|---------|-------|
| 1 | `find_semantic_duplicates` | 1381 | 1438 | 2 |
| 2 | `find_hotspots` | 443 | 723 | 3 |
| 3 | `get_changed_symbols` | 428 | 465 | 4 |
| 4 | `find_impacted_test_files` | 417 | 481 | 4 |
| 5 | `find_symbol` | 404 | 614 | 16 |

## 4. Top 5 retry patterns (same tool, distinct args, same task)

| # | Task | Tool | Calls | Distinct args |
|---|------|------|-------|---------------|
| 1 | TASK-022 | `get_function_source` | 15 | 15 |
| 2 | TASK-043 | `get_functions` | 13 | 13 |
| 3 | TASK-031 | `get_env_usage` | 11 | 11 |
| 4 | TASK-052 | `get_community` | 10 | 10 |
| 5 | TASK-026 | `get_imports` | 7 | 7 |

**Sample arg sets:**

- `get_function_source` in TASK-022:
  - `{"hints": false, "level": 0, "name": "buggy_paginate"}`
  - `{"hints": false, "level": 0, "name": "refund_payment"}`
  - `{"hints": false, "level": 0, "name": "truncate"}`
- `get_functions` in TASK-043:
  - `{"file_path": "apps/api/services/webhooks.py", "hints": false}`
  - `{"file_path": "apps/api/services/exports.py", "hints": false}`
  - `{"file_path": "apps/api/services/complex_auth.py", "hints": false}`
- `get_env_usage` in TASK-031:
  - `{"var_name": "ALLOWED_ORIGINS"}`
  - `{"var_name": "LOG_LEVEL"}`
  - `{"var_name": "TSBENCH_HIDDEN_REGION"}`
- `get_community` in TASK-052:
  - `{"name": "medium_util__n6"}`
  - `{"name": "_notifications_admin_db__n6"}`
  - `{"name": "_billing_admin_db__n7"}`
- `get_imports` in TASK-026:
  - `{"file_path": "apps/api/ambig/mod2.py"}`
  - `{"file_path": "apps/api/cycles/mod_x.py"}`
  - `{"file_path": "apps/api/cycles/mod_a.py"}`

## 5. Top 5 closing tools (last TS call before final answer)

| # | Tool | Tasks closed |
|---|------|--------------|
| 1 | `search_codebase` | 12 |
| 2 | `get_dependents` | 5 |
| 3 | `get_function_source` | 5 |
| 4 | `get_full_context` | 4 |
| 5 | `list_files` | 4 |

## 6. Recommendations

- **Empty-result hotspot: `list_files` (8 empty calls).** Return a `suggestions` field (closest symbols by edit distance, fuzzy file matches) so the agent doesn't have to re-query blindly.
- **Chain `get_function_source -> get_function_source -> get_function_source` appears 24×.** Introduce a combined tool that returns the symbol location, source, and dependents/dependencies in one response (e.g. `get_full_context`).
- **`find_semantic_duplicates` is slowest (median 1381ms, peak 1438ms, 2 calls).** Priority for caching / index pre-computation.
- **Retry pattern on `get_function_source` (15 calls, 15 distinct arg sets in task TASK-022).** First response format is insufficient — enrich output (e.g. broader match set, result preview, disambiguation hints).
- **`search_codebase` closes 12 tasks.** Audit its response format: it is the last thing the agent sees before answering, so it must be concise, complete, and answer-shaped.
