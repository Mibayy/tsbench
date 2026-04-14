# tsbench

A synthetic benchmark project for evaluating MCP code-navigation servers.

## Purpose

`tsbench` measures how efficiently different code-intelligence tools answer realistic engineering questions on a known codebase. It is designed to A/B compare:

- **Plain** baseline — `Read` / `Grep` / `Glob` / `Bash` only
- **LSP** baseline — language-server-based navigation
- **Token Savior** — structural code navigation MCP

over a **40-task suite** covering localization, impact analysis, structural edits, change review, dead-code detection, config audits, Docker inspection, test selection, debugging, and onboarding.

## What's in the repo

| Path | What |
|---|---|
| `generate.py` | Reproducible generator (`--seed 42`) that produces the synthetic project |
| `breaking_changes.py` | Applies 6 intentional breaking changes between `v1` and `v2` tags |
| `GROUND_TRUTH.json` | Documented artifacts planted in the project — the oracle used to score runs |
| `apps/` `packages/` `infra/` `config/` ... | The generated synthetic project itself |

## Why synthetic?

A generated project lets us **know the ground truth by construction**. Every dead function, every call chain, every hotspot, every duplicate pair, every breaking change is planted deterministically and indexed in `GROUND_TRUTH.json`. No manual labeling, no subjective judgments — runs are scored against the oracle.

## Planted artifacts

| ID prefix | What | Count |
|---|---|---|
| `DEAD-*` | Exported functions never called | 12 |
| `HOTSPOT-*` | High cyclomatic complexity (≥12) | 5 |
| `CALLER-*` | Symbols with known N callers (1,3,8,20) | 4 |
| `CHAIN-*` | Known A→B→C→D call chains | 3 |
| `CYCLE-*` | Intentional circular dependencies | 2 |
| `BREAK-*` | Breaking changes between v1 and v2 | 6 |
| `SECRET-*` | Fake secrets in `.env.staging` | 3 |
| `ORPHAN-*` | Env vars declared but never read | 4 |
| `UNDECL-*` | Env vars read but not declared | 2 |
| `DUP-*` | Semantically duplicated function pairs | 3 |
| `DOCKER-*` | Dockerfile issues | 2 |
| `BUG-*` | Planted bugs (off-by-one, pagination) | 2 |
| `AMBIG-*` | Cross-module name collisions | 2 |

## Reproduce

```bash
python3 generate.py --seed 42
git add -A && git commit -m "tsbench v1" && git tag v1
python3 breaking_changes.py
git add -A && git commit -m "tsbench v2 (breaking changes)" && git tag v2
```

## License

MIT — use freely for benchmarking your own code-navigation tooling.
