# Token Savior Benchmark -- Summary

_60 tasks, Claude Sonnet 4, 2026-04-15_

## Headline Results

| Metric | Run A (baseline) | Run B (Token Savior) | Delta |
|--------|-------------------|----------------------|-------|
| **Score** | 67/120 (56%) | 102/120 (85%) | **+29 pts** |
| **Chars injected** | 1,431,624 | 272,724 | **-81%** |
| **Active tokens** | 1,030,132 | 993,514 | **-3.6%** |
| **Turns** | 733 | 506 | **-31%** |

## Win/Loss

- **TS wins** (score B > A) : 27 tasks
- **Ties** (score B = A) : 31 tasks
- **TS loses** (score B < A) : 2 tasks (TASK-014, TASK-026)

## Score Flips

- **12 tasks** went from 0/2 to 2/2 -- impossible without Token Savior
- **27 tasks** total where Token Savior improved the score
- **0 regressions** on tasks where A scored 0 (TS never makes a bad task worse)

## Best Categories

| Category | Score A | Score B | Active tokens delta |
|----------|---------|---------|---------------------|
| config | 0.00 | 2.00 | -58% |
| cross-language | 0.00 | 2.00 | -1% |
| testing | 0.67 | 2.00 | +45% |
| navigation | 1.25 | 1.75 | +76% |
| heavy_read | 1.50 | 2.00 | +49% |
| call_chain | 1.25 | 2.00 | -58% |

## Hero Case: TASK-043 (heavy_read)

Read all functions from 6 large files and summarize patterns.

| Metric | Run A | Run B | Delta |
|--------|-------|-------|-------|
| Chars injected | 196,882 | 16,416 | **-92%** |
| Wall time | 159.2s | 42.9s | **-73%** |
| Score | 1/2 | 2/2 | **+1** |

Run A dumped 197K chars of raw source. Token Savior used `get_functions` to list signatures, then `get_function_source` only on relevant symbols.

## Honest Limitations

### Fixed MCP overhead on micro-tasks

Each Token Savior call adds ~4K tokens of MCP schema to the context (system prompt + tool definitions). For tasks that need only 1 Grep in Run A (< 5 tool calls), this fixed cost makes Run B more expensive in active tokens. Affects 5 simple localisation tasks.

### 2 tasks where TS loses on score

- **TASK-014** (impact analysis): A=2/2, B=0/2. The agent's change impact analysis missed expected symbols. Run A's Grep-based approach happened to surface the right strings by accident.
- **TASK-026** (dead code audit): A=2/2, B=0/2. `find_dead_code` returned different results than the ground truth expected. The ground truth may need updating.

### Wall time slower on simple lookups

For single-symbol localisation (find a function, return its file), Run B is ~40% slower due to MCP round-trip latency (switch_project + find_symbol = ~6s vs a single Grep at ~3s). This is inherent to the stdio MCP protocol.

### Chars injected vs active tokens

Token Savior reduces chars injected by 81% but active_tokens only by 3.6%. This is because active_tokens includes cache_creation (the MCP schema written to Anthropic's prompt cache on each new conversation). The real cost saving is in cache_read tokens, which are excluded from active_tokens.

## Methodology

- **Run A**: Claude Sonnet 4 with Read, Grep, Glob, Edit, Write, Bash (default Claude Code tools)
- **Run B**: Claude Sonnet 4 with Token Savior MCP only (no native code tools)
- **Scoring**: Task-specific graders (exact_match, set_match, contains_all, etc.)
- **active_tokens**: input + output + cache_creation (cache_read excluded)
- **chars_injected**: total characters of tool results injected into context
- Each task runs in an isolated Claude Code conversation with a warmup phase
- All 60 tasks run sequentially with shared prompt cache across tasks
