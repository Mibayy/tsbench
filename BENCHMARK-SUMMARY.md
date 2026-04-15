# tsbench -- Benchmark Summary

## Overview

60 tasks total covering 12 categories, testing Token Savior MCP vs plain Claude Code.

- **Run A** (baseline): Claude Code without MCP, using Read/Grep/Glob
- **Run B** (Token Savior): Claude Code + token-savior MCP, Read/Grep/Glob disallowed

## Results (60 tasks)

### Paired tasks (A+B both run): 20 tasks

| Metric | Run A | Run B | Delta |
|--------|-------|-------|-------|
| Score | 29/40 (72%) | 35/40 (88%) | **+16pp** |
| Active tokens | 369,978 | 401,521 | -8.5% |
| Chars injected | 336,123 | 61,709 | **+82%** |
| Wall time avg | 25.3s | 32.0s | +26% |

**TS gagne** : 5 | **Ex aequo** : 15 | **TS perd** : 0

### B-only tasks (TASK-047 to TASK-060): 14 tasks

| Score | 27/28 (96%) |
|-------|-------------|
| Avg wall time | 27.0s |
| Avg active tokens | 16,261 |

### Score global Run B (toutes 34 taches executees)

**62/68 (91%)**

## Key findings

1. **Score superieur** : +16pp sur les taches appariees (72% -> 88%)
2. **Chars injected -82%** : Token Savior injecte 5x moins de contexte
3. **Tache impossible sans TS** : TASK-045 (auth-importers) score 0 en A, 2/2 en B
4. **call_chain** : 1.00 -> 2.00 (score moyen double)
5. **heavy_read** : 1.50 -> 2.00 (score moyen +33%)
6. **14 nouveaux outils testes** : get_file_dependencies, get_file_dependents, get_call_chain, get_backward_slice, get_entry_points, get_community, find_semantic_duplicates, replace_symbol_source, insert_near_symbol, create_checkpoint, find_impacted_test_files, find_hotspots, get_git_status, get_changed_symbols

## Tool coverage

14 new tasks (TASK-047 to TASK-060) added to cover previously untested tools:

| Task | Tool tested | Score | Category |
|------|------------|-------|----------|
| 047 | get_file_dependencies | 2/2 | navigation |
| 048 | get_file_dependents | 2/2 | navigation |
| 049 | get_call_chain (forced) | 2/2 | call_chain |
| 050 | get_backward_slice | 1/2 | navigation |
| 051 | get_entry_points | 2/2 | navigation |
| 052 | get_community | 2/2 | audit |
| 053 | find_semantic_duplicates | 2/2 | audit |
| 054 | replace_symbol_source | 2/2 | edit |
| 055 | insert_near_symbol | 2/2 | edit |
| 056 | create_checkpoint + compare | 2/2 | edit |
| 057 | find_impacted_test_files | 2/2 | testing |
| 058 | find_hotspots | 2/2 | audit |
| 059 | get_git_status | 2/2 | git |
| 060 | get_changed_symbols | 2/2 | git |

## Per-task disallowed_tools

bench.py now supports per-task `disallowed_tools` in index.json, merged with base `Read,Grep,Glob`:

- TASK-049: `get_dependencies, get_dependents` disallowed (forces get_call_chain)
- TASK-054/055/056: `Edit, Write` disallowed (forces structural edit tools)

## Remaining gaps

- 26 tasks (TASK-015 to TASK-040) have no Run B data yet
- Run A missing for TASK-047 to TASK-060 (B-only tasks)
- Some tools still untested: get_routes, get_feature_files, corpus_build/query, pack_context
