# tsbench -- Benchmark Summary

## Overview

60 tasks total covering 16 categories, testing Token Savior MCP vs plain Claude Code.

- **Run A** (baseline): Claude Code without MCP, using Read/Grep/Glob
- **Run B** (Token Savior): Claude Code + token-savior MCP, Read/Grep/Glob disallowed

## Results (60/60 paired runs)

| Metric | Run A | Run B | Delta |
|--------|-------|-------|-------|
| Score | 67/120 (56%) | 73/120 (61%) | **+5pp** |
| Chars injected | 1,431,624 | 305,864 | **-79%** |
| Wall time avg | 51.0s | 36.6s | **-28%** |
| Turns cumules | 733 | 625 | -15% |

**TS gagne** : 7 | **Ex aequo** : 51 | **TS perd** : 2

## Key findings

1. **Chars injected -79%** : Token Savior injecte ~5x moins de contexte dans la fenetre
2. **28% plus rapide** : wall time moyen 51s -> 36.6s
3. **Score +5pp** : 56% -> 61% (7 victoires, 2 defaites)
4. **2 taches impossibles sans TS** : TASK-045 (auth-importers) et TASK-047 (file-deps) score 0 en A, 2/2 en B
5. **call_chain** : 1.25 -> 2.00 (score moyen +60%)
6. **heavy_read** : 1.50 -> 2.00 (score moyen +33%)
7. **Audit massif** : TASK-052 chars 190k->3.7k (-98%), TASK-058 chars 162k->6k (-96%)

## Top categories for Token Savior

| Categorie | Score A | Score B | Chars reduction | Speed |
|-----------|---------|---------|-----------------|-------|
| audit | 1.33 | 1.33 | +36% active | -71% wall |
| heavy_read | 1.50 | 2.00 | +12% active | -35% wall |
| call_chain | 1.25 | 2.00 | -11% active | +179% wall |
| navigation | 1.25 | 1.75 | +47% active | -32% wall |
| testing | 0.67 | 0.67 | +56% active | -17% wall |

## Tool coverage

14 tasks (TASK-047 to TASK-060) cover previously untested tools:

| Task | Tool tested | Score A | Score B | Category |
|------|------------|---------|---------|----------|
| 047 | get_file_dependencies | 0/2 | 2/2 | navigation |
| 048 | get_file_dependents | 2/2 | 2/2 | navigation |
| 049 | get_call_chain (forced) | 2/2 | 2/2 | call_chain |
| 050 | get_backward_slice | 1/2 | 1/2 | navigation |
| 051 | get_entry_points | 2/2 | 2/2 | navigation |
| 052 | get_community | 2/2 | 2/2 | audit |
| 053 | find_semantic_duplicates | 2/2 | 2/2 | audit |
| 054 | replace_symbol_source | 2/2 | 2/2 | edit |
| 055 | insert_near_symbol | 2/2 | 2/2 | edit |
| 056 | create_checkpoint + compare | 2/2 | 2/2 | edit |
| 057 | find_impacted_test_files | 2/2 | 2/2 | testing |
| 058 | find_hotspots | 2/2 | 2/2 | audit |
| 059 | get_git_status | 2/2 | 2/2 | git |
| 060 | get_changed_symbols | 2/2 | 2/2 | git |

## Per-task disallowed_tools

bench.py supports per-task `disallowed_tools` in index.json, merged with base `Read,Grep,Glob`:

- TASK-049: `get_dependencies, get_dependents` disallowed (forces get_call_chain)
- TASK-054/055/056: `Edit, Write` disallowed (forces structural edit tools)

## Remaining gaps

- Some tools still untested: get_routes, get_feature_files, corpus_build/query, pack_context
- Instrumentation (ts_tool_details per call) not yet implemented
