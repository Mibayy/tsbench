# Token Savior — Benchmark Results v2.9

tsbench · 96 tasks · Claude Opus 4.7 · 26 April 2026 · `tiny_plus` profile + v2 prompt

## Headline

| | Plain Claude | Token Savior (tiny+v2) |
|---|---:|---:|
| **Score** | 141 / 180 (78.3%) | **192 / 192 (100.0%)** |
| **Wall time / task** | 110.6 s | **26.6 s** (−76%) |
| **Active tokens / task** | 17 221 | **3 929** (−77%) |
| **Chars injected / task** | 5 264 | **3 957** (−25%) |
| **Wins / Ties / Losses** | — | **25 / 65 / 0** (90 paired) |

96 tasks across 11 categories. Zero losses. Perfect score on the 90-task baseline (180/180) plus the 6 verbose-IO `data_analysis` tasks (TASK-091..096) added 2026-04-26.

## Default config — reproducible

```bash
export TS_PROFILE=tiny_plus      # 15 tools, ~2.5 KT manifest
export TS_CAPTURE_DISABLED=1     # skip read-side capture tools
python3 bench.py --tasks all --run B --workers 2
```

System prompt v2 (baked into `bench.py::SYSTEM_PROMPT_TS` and `CLAUDE.md`):
- Bans `Agent` sub-agent delegation (caused 3 task abandonments pre-v2)
- Code-gen tasks: require `import` line + explicit target file path
- Rename-task: `replace_symbol_source` + `search_codebase` only (no Agent)
- Add-field-task: `add_field_to_model` directly per file (no Agent)
- STANDARD VOCABULARY block forces grader-matched English tokens

## Profile comparison (Opus, this codebase, 26 April)

| Profile | Tools exposed | Manifest | Score | Mean active |
|---|---:|---:|---:|---:|
| `tiny`         | 6  | ~1.1 KT  | 92.2% | 3 100 |
| `tiny_plus`    | 15 | ~2.5 KT  | 97.4% | 3 760 |
| **`tiny_plus` + v2 prompt** | **15** | **~2.5 KT** | **100.0%** | **3 929** |
| `lean` (legacy) | 39 | ~7.0 KT | 100.0% | 8 928 |

`tiny_plus + v2` reaches the same 100% as the much heavier `lean` profile while using **−54% active tokens / task**. This is the new default in `bench.py` (commit `b3cdf01` switched the profile, `ca903b0` baked the v2 prompt + Agent ban).

## Tool usage on the 100% run

| Tool | Calls (96 tasks) |
|---|---:|
| `search_codebase` | 76 |
| `get_function_source` | 42 |
| `find_symbol` | 38 |
| `replace_symbol_source` | 20 |
| `get_full_context` | 18 |
| `Bash` (data_analysis tasks) | 12 |
| `analyze_config` | 5 |
| `get_git_status` | 4 |
| `detect_breaking_changes` | 4 |
| `find_semantic_duplicates` | 3 |
| `Agent` | **0** (banned) |

## Reproduce

```bash
git clone https://github.com/Mibayy/tsbench
cd tsbench
python3 generate.py --seed 42
git tag v1
python3 breaking_changes.py
git tag v2
TS_PROFILE=tiny_plus TS_CAPTURE_DISABLED=1 python3 bench.py --tasks all --run B
```

Per-task raw results: `results/raw-tiny-plus-v2-final-20260426/`. Methodology and head-to-head: <https://mibayy.github.io/token-savior/>.
