# matrix.json schema

Consolidated results for the 6-config benchmark (3 models x 2 modes).
Produced by `scripts/build_matrix.py` from `results/raw-{config_id}/*.json`.
Consumed by the picker on the site to let the visitor pick any config pair.

**Task universe = `tasks/index.json` (90 tasks, non-contiguous IDs up to
TASK-111).** Raw results for dropped task IDs are ignored during build.

## Config IDs

Stable identifier = `{model_short}-{mode}`.

| config_id     | model                       | mode  | bench.py run |
|---------------|-----------------------------|-------|--------------|
| `opus-base`   | claude-opus-4-7             | base  | A            |
| `opus-ts`     | claude-opus-4-7             | ts    | B            |
| `sonnet-base` | claude-sonnet-4-6           | base  | A            |
| `sonnet-ts`   | claude-sonnet-4-6           | ts    | B            |
| `haiku-base`  | claude-haiku-4-5-20251001   | base  | A            |
| `haiku-ts`    | claude-haiku-4-5-20251001   | ts    | B            |

- `base` = no MCP, no system prompt, no disallowed tools (native Claude Code).
- `ts`   = token-savior MCP + TS system prompt + Read/Grep/Glob disallowed.

Run letter is a bench.py internal: A = base, B = ts. It stays stable across
models; the model is selected via `TSBENCH_MODEL` env var.

## Raw layout

Each config owns its own archive directory so running a new config never
clobbers a previous one:

```
results/
  raw/                      # scratch space, holds current/in-progress run
  raw-opus-base/            # archived after Run A (Opus)
  raw-opus-ts/              # archived after Run B (Opus)
  raw-sonnet-base/
  raw-sonnet-ts/
  raw-haiku-base/
  raw-haiku-ts/
  matrix.json               # built from all of the above
```

File naming inside each `raw-{config_id}/`: `TASK-XXX.json` (run suffix dropped
on archive - the config_id already encodes it).

## matrix.json shape

```json
{
  "generated_at": "2026-04-20T18:40:00+00:00",
  "task_count": 111,
  "configs": [
    {
      "id": "opus-base",
      "model": "claude-opus-4-7",
      "mode": "base",
      "run_letter": "A",
      "source_dir": "raw-opus-base",
      "tasks_covered": 111
    }
  ],
  "tasks": {
    "TASK-001": {
      "category": "navigation",
      "difficulty": "easy",
      "scoring": "exact_match",
      "results": {
        "opus-base": {
          "active_tokens": 9421,
          "total_tokens": 120345,
          "turns": 3,
          "tool_calls": 1,
          "wall_time_seconds": 12.3,
          "score": 2,
          "max_score": 2,
          "error": null,
          "context_chars": 5210
        },
        "opus-ts": { "...": "..." }
      }
    }
  },
  "summary": {
    "opus-base": {
      "n_tasks": 111,
      "active_tokens_total": 1234567,
      "active_tokens_mean": 11122,
      "turns_total": 412,
      "score_total": 187,
      "score_max_total": 222,
      "score_pct": 84.2,
      "wall_time_total": 1520.7
    }
  },
  "pairs": {
    "opus": {
      "base": "opus-base",
      "ts":   "opus-ts",
      "reduction_active_pct": 62.4,
      "delta_score": 3,
      "wins_ts": 58,
      "ties": 42,
      "wins_base": 11
    }
  }
}
```

### Per-task result fields

| field               | source (raw)                           | semantics                                             |
|---------------------|----------------------------------------|-------------------------------------------------------|
| `active_tokens`     | `active_tokens`                        | input + output + cache_creation (cache_read excluded) |
| `total_tokens`      | `total_tokens`                         | full token cost including cache_read                  |
| `turns`             | `turns_count`                          | assistant turns                                       |
| `tool_calls`        | `tool_calls_count`                     |                                                       |
| `wall_time_seconds` | `wall_time_seconds`                    |                                                       |
| `score`             | `score`                                | 0-2                                                   |
| `max_score`         | `max_score`                            | always 2 today                                        |
| `error`             | `error`                                | null if OK                                            |
| `context_chars`     | `total_context_chars_injected`         | sum of tool-result chars injected                     |

A task missing from a config (crash, skipped, not yet run) gets `null` in
`results[config_id]` rather than being absent - the picker can distinguish
"not run" from "run with error".

### Summary metric

Primary metric is `active_tokens` (matches `bench.py::generate_report`).
`score_pct = score_total / score_max_total * 100`.

### Pairs

For each model, we precompute the A-vs-B comparison over tasks present in
both configs. `reduction_active_pct = (active_A - active_B) / active_A * 100`.
`wins_ts` counts tasks where TS strictly beats base on score.
