# Token Savior — Improvement Signals (Run B)

_Analyzed 60 tasks, 466 TS tool calls._

## 1. Top 10 empty calls (`result_chars < 50`)

| # | Task | Tool | Args | Chars |
|---|------|------|------|-------|
| 1 | TASK-050 | `get_dependencies` | `{"name": "reconcile_payments"}` | 2 |
| 2 | TASK-019 | `get_imports` | `{"file_path": "packages/utils/paginate_copy.py"}` | 2 |
| 3 | TASK-026 | `get_imports` | `{"file_path": "apps/api/cycles/__init__.py"}` | 2 |
| 4 | TASK-026 | `get_imports` | `{"file_path": "apps/api/chains/alpha.py"}` | 2 |
| 5 | TASK-026 | `get_imports` | `{"file_path": "apps/api/chains/beta.py"}` | 2 |
| 6 | TASK-026 | `get_imports` | `{"file_path": "apps/api/chains/gamma.py"}` | 2 |
| 7 | TASK-018 | `list_files` | `{"pattern": "*schema.prisma*"}` | 2 |
| 8 | TASK-030 | `list_files` | `{"pattern": "**/Dockerfile*"}` | 2 |
| 9 | TASK-032 | `list_files` | `{"pattern": "*test*complex_billing*"}` | 2 |
| 10 | TASK-033 | `list_files` | `{"pattern": "*test*alpha*"}` | 2 |

## 2. Top 5 chaining sequences (A -> B -> C)

| # | Chain | Frequency |
|---|-------|-----------|
| 1 | `get_function_source` -> `get_function_source` -> `get_function_source` | 46 |
| 2 | `get_functions` -> `get_functions` -> `get_functions` | 15 |
| 3 | `search_codebase` -> `search_codebase` -> `search_codebase` | 9 |
| 4 | `get_structure_summary` -> `get_structure_summary` -> `get_structure_summary` | 8 |
| 5 | `get_community` -> `get_community` -> `get_community` | 8 |

**Top 5 pairs (A -> B):**

| # | Pair | Frequency |
|---|------|-----------|
| 1 | `get_function_source` -> `get_function_source` | 72 |
| 2 | `search_codebase` -> `search_codebase` | 19 |
| 3 | `get_functions` -> `get_functions` | 19 |
| 4 | `switch_project` -> `find_symbol` | 17 |
| 5 | `list_files` -> `list_files` | 15 |

## 3. Top 5 slowest tools (median `time_ms`)

| # | Tool | Median ms | Peak ms | Calls |
|---|------|-----------|---------|-------|
| 1 | `find_semantic_duplicates` | 1237 | 1239 | 2 |
| 2 | `find_symbol` | 488 | 935 | 28 |
| 3 | `get_file_dependencies` | 404 | 552 | 11 |
| 4 | `find_hotspots` | 362 | 374 | 2 |
| 5 | `get_function_source` | 336 | 795 | 107 |

## 4. Top 5 retry patterns (same tool, distinct args, same task)

| # | Task | Tool | Calls | Distinct args |
|---|------|------|-------|---------------|
| 1 | TASK-022 | `get_function_source` | 13 | 13 |
| 2 | TASK-043 | `get_functions` | 13 | 13 |
| 3 | TASK-041 | `get_function_source` | 12 | 12 |
| 4 | TASK-052 | `get_community` | 10 | 10 |
| 5 | TASK-026 | `get_file_dependencies` | 9 | 9 |

**Sample arg sets:**

- `get_function_source` in TASK-022:
  - `{"file_path": "packages/utils/slug_copy.py", "level": 0, "name": "to_slug"}`
  - `{"level": 0, "name": "paginate_also"}`
  - `{"level": 0, "name": "generate_report"}`
- `get_functions` in TASK-043:
  - `{"file_path": "apps/api/services/sessions.py"}`
  - `{"file_path": "apps/api/services/audit.py"}`
  - `{"file_path": "apps/api/services/auth.py"}`
- `get_function_source` in TASK-041:
  - `{"file_path": "apps/api/services/billing.py", "level": 0, "name": "list_invoices"}`
  - `{"file_path": "apps/api/services/billing.py", "level": 1, "name": "calculate_invoice"}`
  - `{"file_path": "apps/api/services/billing.py", "level": 1, "name": "apply_discount"}`
- `get_community` in TASK-052:
  - `{"name": "TopBar__n22"}`
  - `{"name": "_billing_admin_db__n7"}`
  - `{"name": "_webhooks_admin_db__n6"}`
- `get_file_dependencies` in TASK-026:
  - `{"file_path": "apps/api/cycles/__init__.py"}`
  - `{"file_path": "apps/api/cycles/mod_x.py"}`
  - `{"file_path": "apps/api/cycles/mod_y.py"}`

## 5. Top 5 closing tools (last TS call before final answer)

| # | Tool | Tasks closed |
|---|------|--------------|
| 1 | `search_codebase` | 15 |
| 2 | `get_function_source` | 14 |
| 3 | `get_dependents` | 4 |
| 4 | `get_class_source` | 4 |
| 5 | `find_impacted_test_files` | 2 |

## 6. Recommendations

- **Empty-result hotspot: `get_imports` (5 empty calls).** Return a `suggestions` field (closest symbols by edit distance, fuzzy file matches) so the agent doesn't have to re-query blindly.
- **Chain `get_function_source -> get_function_source -> get_function_source` appears 46×.** Introduce a combined tool that returns the symbol location, source, and dependents/dependencies in one response (e.g. `get_full_context`).
- **`find_semantic_duplicates` is slowest (median 1237ms, peak 1239ms, 2 calls).** Priority for caching / index pre-computation.
- **Retry pattern on `get_function_source` (13 calls, 13 distinct arg sets in task TASK-022).** First response format is insufficient — enrich output (e.g. broader match set, result preview, disambiguation hints).
- **`search_codebase` closes 15 tasks.** Audit its response format: it is the last thing the agent sees before answering, so it must be concise, complete, and answer-shaped.
