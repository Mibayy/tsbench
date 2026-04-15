# IMPROVEMENT-SIGNALS.md

_Generated 2026-04-15T17:28:30.028774Z from 60 Run B results, 408 TS tool calls._

## 1. Tool Usage Overview

- **Total TS tool calls**: 408
- **Unique tools used**: 41
- **Empty results**: 62 (15%)
- **Errors**: 0
- **Avg calls/task**: 6.8

| Tool | Count | Avg ms | Avg chars | Empty rate |
|------|------:|-------:|----------:|----------:|
| switch_project | 60 | 118 | 60 | 0% |
| get_function_source | 60 | 378 | 508 | 8% |
| search_codebase | 50 | 244 | 1940 | 10% |
| get_structure_summary | 38 | 183 | 313 | 10% |
| list_files | 32 | 223 | 144 | 50% |
| get_full_context | 22 | 274 | 1023 | 4% |
| get_functions | 21 | 303 | 1251 | 19% |
| find_symbol | 16 | 413 | 58 | 31% |
| get_imports | 11 | 262 | 99 | 63% |
| get_env_usage | 11 | 317 | 1294 | 0% |
| get_community | 10 | 221 | 317 | 0% |
| get_class_source | 9 | 335 | 449 | 11% |
| memory_search | 9 | 115 | 32 | 100% |
| get_dependents | 7 | 314 | 575 | 0% |
| get_file_dependents | 5 | 194 | 146 | 60% |
| find_impacted_test_files | 4 | 344 | 142 | 0% |
| get_changed_symbols | 4 | 417 | 4945 | 0% |
| analyze_config | 4 | 144 | 4168 | 0% |
| get_change_impact | 3 | 388 | 72 | 0% |
| find_hotspots | 3 | 427 | 2118 | 0% |
| replace_symbol_source | 3 | 74 | 200 | 0% |
| insert_near_symbol | 2 | 52 | 178 | 0% |
| detect_breaking_changes | 2 | 370 | 1353 | 0% |
| get_project_summary | 2 | 400 | 248 | 0% |
| analyze_docker | 2 | 329 | 67 | 0% |
| find_semantic_duplicates | 2 | 1381 | 9550 | 0% |
| get_entry_points | 2 | 242 | 3408 | 0% |
| get_classes | 1 | 54 | 32 | 100% |
| memory_get | 1 | 69 | 247 | 0% |
| find_dead_code | 1 | 447 | 380 | 0% |
| find_cross_project_deps | 1 | 55 | 85 | 0% |
| pack_context | 1 | 84 | 2109 | 0% |
| get_routes | 1 | 236 | 957 | 0% |
| get_file_dependencies | 1 | 341 | 120 | 0% |
| get_call_chain | 1 | 376 | 241 | 0% |
| get_backward_slice | 1 | 67 | 940 | 0% |
| get_leiden_stats | 1 | 30 | 481 | 0% |
| reindex | 1 | 2162 | 42 | 100% |
| create_checkpoint | 1 | 287 | 89 | 0% |
| compare_checkpoint_by_symbol | 1 | 68 | 160 | 0% |
| get_git_status | 1 | 75 | 1548 | 0% |

## 2. Empty Results (top 20)

Calls that returned empty or near-empty results. Indicates the agent searched in the wrong place or used wrong args.

| Task | Tool | Args (truncated) |
|------|------|-----------------|
| TASK-005 | search_codebase | `{"pattern": "table.*association_member|members.*table|CREATE TABLE.*member", "ma` |
| TASK-015 | get_file_dependents | `{"file_path": "apps/api/cycles/mod_a.py"}` |
| TASK-015 | get_file_dependents | `{"file_path": "apps/api/cycles/mod_b.py"}` |
| TASK-017 | search_codebase | `{"pattern": "from.*ambig.*mod1|import.*mod1", "project": "tsbench"}` |
| TASK-018 | list_files | `{"pattern": "*schema.prisma*"}` |
| TASK-018 | list_files | `{"pattern": "*prisma*"}` |
| TASK-019 | memory_search | `{"query": "DEFAULT_PAGE_SIZE page size constant"}` |
| TASK-019 | list_files | `{"pattern": "apps/web/constants*"}` |
| TASK-019 | list_files | `{"pattern": "packages/*/constants*"}` |
| TASK-019 | list_files | `{"pattern": "packages/config*"}` |
| TASK-019 | find_symbol | `{"name": "DEFAULT_QUERY", "level": 2}` |
| TASK-019 | find_symbol | `{"name": "INITIAL_STATE", "level": 2}` |
| TASK-019 | get_classes | `{"file_path": "apps/web/api/billing.ts", "hints": false}` |
| TASK-020 | search_codebase | `{"pattern": "from apps\\.api\\.utils\\.strings import"}` |
| TASK-022 | memory_search | `{"query": "v1 v2 changes risk review"}` |
| TASK-023 | memory_search | `{"query": "breaking changes API v1 v2"}` |
| TASK-026 | get_imports | `{"file_path": "apps/api/cycles/mod_a.py"}` |
| TASK-026 | get_imports | `{"file_path": "apps/api/cycles/mod_b.py"}` |
| TASK-026 | get_imports | `{"file_path": "apps/api/cycles/mod_x.py"}` |
| TASK-026 | get_imports | `{"file_path": "apps/api/cycles/mod_y.py"}` |

## 3. Chaining Patterns (bigrams)

Most common tool-to-tool transitions. Self-loops indicate iterative exploration.

| Chain | Count | Type |
|-------|------:|------|
| get_function_source -> get_function_source | 35 | self-loop |
| search_codebase -> search_codebase | 19 | self-loop |
| get_full_context -> get_full_context | 13 | self-loop |
| list_files -> list_files | 13 | self-loop |
| get_structure_summary -> get_structure_summary | 13 | self-loop |
| get_functions -> get_functions | 12 | self-loop |
| get_env_usage -> get_env_usage | 9 | self-loop |
| get_community -> get_community | 9 | self-loop |
| list_files -> get_structure_summary | 8 | sequence |
| get_structure_summary -> get_function_source | 8 | sequence |
| switch_project -> get_full_context | 7 | sequence |
| switch_project -> memory_search | 7 | sequence |
| get_imports -> get_imports | 7 | self-loop |
| switch_project -> search_codebase | 6 | sequence |
| switch_project -> find_symbol | 5 | sequence |

## 4. Top Sequences (trigrams)

| Sequence | Count |
|----------|------:|
| get_function_source -> get_function_source -> get_function_source | 24 |
| get_functions -> get_functions -> get_functions | 11 |
| search_codebase -> search_codebase -> search_codebase | 10 |
| get_full_context -> get_full_context -> get_full_context | 9 |
| get_community -> get_community -> get_community | 8 |
| get_env_usage -> get_env_usage -> get_env_usage | 7 |
| get_structure_summary -> get_structure_summary -> get_structure_summary | 7 |
| list_files -> list_files -> list_files | 6 |
| get_structure_summary -> get_structure_summary -> get_function_source | 5 |
| get_structure_summary -> get_function_source -> get_function_source | 5 |

## 5. Slowest Tools

| Tool | Avg ms | Max ms | N | Total ms |
|------|-------:|-------:|--:|---------:|
| reindex | 2162 | 2162 | 1 | 2162 |
| find_semantic_duplicates | 1381 | 1438 | 2 | 2762 |
| find_dead_code | 447 | 447 | 1 | 447 |
| find_hotspots | 427 | 723 | 3 | 1282 |
| get_changed_symbols | 417 | 465 | 4 | 1669 |
| find_symbol | 412 | 614 | 16 | 6604 |
| get_project_summary | 400 | 513 | 2 | 801 |
| get_change_impact | 387 | 711 | 3 | 1163 |
| get_function_source | 377 | 662 | 60 | 22663 |
| get_call_chain | 376 | 376 | 1 | 376 |

## 6. Retry Patterns

Consecutive calls to same tool: **139** occurrences

| Tool | Retry count | % of total calls |
|------|------------:|----------------:|
| get_function_source | 35 | 58% |
| search_codebase | 19 | 38% |
| get_full_context | 13 | 59% |
| list_files | 13 | 40% |
| get_structure_summary | 13 | 34% |
| get_functions | 12 | 57% |
| get_env_usage | 9 | 81% |
| get_community | 9 | 90% |
| get_imports | 7 | 63% |
| find_symbol | 5 | 31% |

## 7. Recommendations

### High empty-result tools

- **list_files**: 16/32 empty (50%) -- consider better defaults or error messages
- **memory_search**: 9/9 empty (100%) -- consider better defaults or error messages
- **get_imports**: 7/11 empty (63%) -- consider better defaults or error messages
- **search_codebase**: 5/50 empty (10%) -- consider better defaults or error messages
- **find_symbol**: 5/16 empty (31%) -- consider better defaults or error messages
- **get_function_source**: 5/60 empty (8%) -- consider better defaults or error messages
- **get_structure_summary**: 4/38 empty (10%) -- consider better defaults or error messages
- **get_functions**: 4/21 empty (19%) -- consider better defaults or error messages
- **get_file_dependents**: 3/5 empty (60%) -- consider better defaults or error messages

### Self-loop reduction

- **get_function_source**: 35 consecutive calls -- could benefit from batch/multi mode
- **search_codebase**: 19 consecutive calls -- could benefit from batch/multi mode
- **get_full_context**: 13 consecutive calls -- could benefit from batch/multi mode
- **list_files**: 13 consecutive calls -- could benefit from batch/multi mode
- **get_structure_summary**: 13 consecutive calls -- could benefit from batch/multi mode

### Performance

- **reindex**: avg 2162ms -- consider caching or optimization
- **find_semantic_duplicates**: avg 1381ms -- consider caching or optimization
- **find_dead_code**: avg 447ms -- consider caching or optimization

### Coverage gaps

Tools never called in benchmark: 19
- `get_dependencies`
- `get_feature_files`
- `corpus_build`
- `corpus_query`
- `list_checkpoints`
- `restore_checkpoint`
- `run_impacted_tests`
- `build_commit_summary`
- `summarize_patch_by_symbol`
- `memory_save`
- `get_duplicate_classes`
- `get_components`
- `get_coactive_symbols`
- `get_relevance_cluster`
- `get_symbol_cluster`
- `get_edit_context`
- `discover_project_actions`
- `run_project_action`
- `apply_symbol_change_and_validate`