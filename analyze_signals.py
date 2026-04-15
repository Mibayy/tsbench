#!/usr/bin/env python3
"""Analyze Run B ts_tool_details and emit results/IMPROVEMENT-SIGNALS.md.

Signals extracted:
  1. Top empty calls (result_chars < 50): tool + args + task
  2. Top chaining sequences A -> B -> C (frequency)
  3. Top slow tools (median time_ms)
  4. Top retry patterns: same tool called N>=2 times with different args in same task
  5. Concrete recommendations per signal
"""
from __future__ import annotations

import json
import statistics
from collections import Counter, defaultdict
from pathlib import Path

RAW_DIR = Path(__file__).parent / "results" / "raw"
OUT_PATH = Path(__file__).parent / "results" / "IMPROVEMENT-SIGNALS.md"


def _args_fingerprint(args: dict) -> str:
    if not isinstance(args, dict):
        return str(args)[:120]
    try:
        return json.dumps(args, sort_keys=True, ensure_ascii=False)[:160]
    except Exception:
        return str(args)[:120]


def load_tasks() -> dict[str, list[dict]]:
    tasks: dict[str, list[dict]] = {}
    for p in sorted(RAW_DIR.glob("TASK-*-run-B.json")):
        task_id = p.stem.replace("-run-B", "")
        try:
            data = json.loads(p.read_text())
        except Exception:
            continue
        details = data.get("ts_tool_details") or []
        tasks[task_id] = details
    return tasks


def analyze(tasks: dict[str, list[dict]]) -> dict:
    empty_calls: list[dict] = []
    chains_3: Counter = Counter()
    chains_2: Counter = Counter()
    tool_times: dict[str, list[int]] = defaultdict(list)
    closing_tools: Counter = Counter()
    retries: list[dict] = []

    for task_id, calls in tasks.items():
        seen_args_by_tool: dict[str, list[str]] = defaultdict(list)

        for i, c in enumerate(calls):
            tool = c.get("tool", "unknown")
            args = c.get("args") or {}
            chars = c.get("result_chars", 0)
            tm = c.get("time_ms")

            if chars is not None and chars < 50:
                empty_calls.append({
                    "task": task_id,
                    "tool": tool,
                    "args": args,
                    "result_chars": chars,
                })

            if isinstance(tm, int):
                tool_times[tool].append(tm)

            prev_t = calls[i - 1].get("tool") if i > 0 else None
            next_t = calls[i + 1].get("tool") if i + 1 < len(calls) else None
            if prev_t and next_t:
                chains_3[(prev_t, tool, next_t)] += 1
            if next_t:
                chains_2[(tool, next_t)] += 1
            if next_t is None:
                closing_tools[tool] += 1

            seen_args_by_tool[tool].append(_args_fingerprint(args))

        for tool, fps in seen_args_by_tool.items():
            unique = set(fps)
            if len(fps) >= 2 and len(unique) >= 2:
                retries.append({
                    "task": task_id,
                    "tool": tool,
                    "count": len(fps),
                    "distinct_args": len(unique),
                    "samples": list(unique)[:3],
                })

    empty_calls.sort(key=lambda x: (x["result_chars"], x["tool"]))
    top_empty = empty_calls[:10]

    top_chains_3 = chains_3.most_common(5)
    top_chains_2 = chains_2.most_common(5)

    slow = []
    for tool, times in tool_times.items():
        if len(times) < 2:
            continue
        slow.append((tool, statistics.median(times), len(times), max(times)))
    slow.sort(key=lambda r: r[1], reverse=True)
    top_slow = slow[:5]

    retries.sort(key=lambda r: (-r["count"], -r["distinct_args"]))
    top_retries = retries[:5]

    top_closing = closing_tools.most_common(5)

    return {
        "top_empty": top_empty,
        "top_chains_3": top_chains_3,
        "top_chains_2": top_chains_2,
        "top_slow": top_slow,
        "top_retries": top_retries,
        "top_closing": top_closing,
        "total_tasks": len(tasks),
        "total_calls": sum(len(v) for v in tasks.values()),
    }


def recommend(sig: dict) -> list[str]:
    recs: list[str] = []

    if sig["top_empty"]:
        tools_hit = Counter(e["tool"] for e in sig["top_empty"])
        top = tools_hit.most_common(1)[0]
        recs.append(
            f"**Empty-result hotspot: `{top[0]}` ({top[1]} empty calls).** "
            f"Return a `suggestions` field (closest symbols by edit distance, "
            f"fuzzy file matches) so the agent doesn't have to re-query blindly."
        )

    if sig["top_chains_3"]:
        (a, b, c), n = sig["top_chains_3"][0]
        recs.append(
            f"**Chain `{a} -> {b} -> {c}` appears {n}×.** "
            f"Introduce a combined tool that returns the symbol location, source, "
            f"and dependents/dependencies in one response (e.g. `get_full_context`)."
        )

    if sig["top_slow"]:
        tool, med, n, mx = sig["top_slow"][0]
        recs.append(
            f"**`{tool}` is slowest (median {int(med)}ms, peak {mx}ms, {n} calls).** "
            f"Priority for caching / index pre-computation."
        )

    if sig["top_retries"]:
        r = sig["top_retries"][0]
        recs.append(
            f"**Retry pattern on `{r['tool']}` ({r['count']} calls, "
            f"{r['distinct_args']} distinct arg sets in task {r['task']}).** "
            f"First response format is insufficient — enrich output "
            f"(e.g. broader match set, result preview, disambiguation hints)."
        )

    if sig["top_closing"]:
        tool, n = sig["top_closing"][0]
        recs.append(
            f"**`{tool}` closes {n} tasks.** "
            f"Audit its response format: it is the last thing the agent sees "
            f"before answering, so it must be concise, complete, and answer-shaped."
        )

    return recs


def render(sig: dict) -> str:
    lines: list[str] = []
    lines.append("# Token Savior — Improvement Signals (Run B)")
    lines.append("")
    lines.append(
        f"_Analyzed {sig['total_tasks']} tasks, {sig['total_calls']} TS tool calls._"
    )
    lines.append("")

    lines.append("## 1. Top 10 empty calls (`result_chars < 50`)")
    lines.append("")
    if not sig["top_empty"]:
        lines.append("_None._")
    else:
        lines.append("| # | Task | Tool | Args | Chars |")
        lines.append("|---|------|------|------|-------|")
        for i, e in enumerate(sig["top_empty"], 1):
            args = _args_fingerprint(e["args"]).replace("|", "\\|")
            lines.append(
                f"| {i} | {e['task']} | `{e['tool']}` | `{args}` | {e['result_chars']} |"
            )
    lines.append("")

    lines.append("## 2. Top 5 chaining sequences (A -> B -> C)")
    lines.append("")
    if not sig["top_chains_3"]:
        lines.append("_None._")
    else:
        lines.append("| # | Chain | Frequency |")
        lines.append("|---|-------|-----------|")
        for i, ((a, b, c), n) in enumerate(sig["top_chains_3"], 1):
            lines.append(f"| {i} | `{a}` -> `{b}` -> `{c}` | {n} |")
    lines.append("")
    if sig["top_chains_2"]:
        lines.append("**Top 5 pairs (A -> B):**")
        lines.append("")
        lines.append("| # | Pair | Frequency |")
        lines.append("|---|------|-----------|")
        for i, ((a, b), n) in enumerate(sig["top_chains_2"], 1):
            lines.append(f"| {i} | `{a}` -> `{b}` | {n} |")
        lines.append("")

    lines.append("## 3. Top 5 slowest tools (median `time_ms`)")
    lines.append("")
    if not sig["top_slow"]:
        lines.append("_None._")
    else:
        lines.append("| # | Tool | Median ms | Peak ms | Calls |")
        lines.append("|---|------|-----------|---------|-------|")
        for i, (tool, med, n, mx) in enumerate(sig["top_slow"], 1):
            lines.append(f"| {i} | `{tool}` | {int(med)} | {mx} | {n} |")
    lines.append("")

    lines.append("## 4. Top 5 retry patterns (same tool, distinct args, same task)")
    lines.append("")
    if not sig["top_retries"]:
        lines.append("_None._")
    else:
        lines.append("| # | Task | Tool | Calls | Distinct args |")
        lines.append("|---|------|------|-------|---------------|")
        for i, r in enumerate(sig["top_retries"], 1):
            lines.append(
                f"| {i} | {r['task']} | `{r['tool']}` | {r['count']} | {r['distinct_args']} |"
            )
        lines.append("")
        lines.append("**Sample arg sets:**")
        lines.append("")
        for r in sig["top_retries"]:
            lines.append(f"- `{r['tool']}` in {r['task']}:")
            for s in r["samples"]:
                lines.append(f"  - `{s}`")
    lines.append("")

    lines.append("## 5. Top 5 closing tools (last TS call before final answer)")
    lines.append("")
    if not sig["top_closing"]:
        lines.append("_None._")
    else:
        lines.append("| # | Tool | Tasks closed |")
        lines.append("|---|------|--------------|")
        for i, (tool, n) in enumerate(sig["top_closing"], 1):
            lines.append(f"| {i} | `{tool}` | {n} |")
    lines.append("")

    lines.append("## 6. Recommendations")
    lines.append("")
    recs = recommend(sig)
    if not recs:
        lines.append("_No signals strong enough to act on._")
    else:
        for r in recs:
            lines.append(f"- {r}")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    tasks = load_tasks()
    if not tasks:
        print("No Run B results found under results/raw/")
        return
    sig = analyze(tasks)
    OUT_PATH.write_text(render(sig))
    print(f"wrote {OUT_PATH} ({sig['total_tasks']} tasks, {sig['total_calls']} calls)")


if __name__ == "__main__":
    main()
