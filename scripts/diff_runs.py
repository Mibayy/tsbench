#!/usr/bin/env python3
"""Diff three Run-B datasets:
  - prev (21/04): results/raw-opus-ts/TASK-*.json
  - baseline (25/04 cur): results/raw-snapshot-20260425-baseline/TASK-*-run-B.json
  - fix (25/04 + optims): results/raw/TASK-*-run-B.json (after re-run)
"""
import json, glob, sys
from statistics import mean, median


def load(pattern):
    return sorted(
        [json.load(open(f)) for f in glob.glob(pattern)],
        key=lambda r: r["task_id"],
    )


def stats(rows, label):
    if not rows:
        return None
    n = len(rows)
    score = sum(r.get("score", 0) for r in rows)
    smax = sum(r.get("score_max", 2) for r in rows)
    active = [r["active_tokens"] for r in rows]
    cc = [r["cache_creation_input_tokens"] for r in rows]
    cr = [r["cache_read_input_tokens"] for r in rows]
    out = [r["output_tokens"] for r in rows]
    tools = [r["tool_calls_count"] for r in rows]
    return {
        "label": label,
        "n": n,
        "score": score,
        "smax": smax,
        "active_mean": mean(active),
        "active_median": median(active),
        "cc_mean": mean(cc),
        "cr_mean": mean(cr),
        "out_mean": mean(out),
        "tools_total": sum(tools),
    }


prev = load("results/raw-opus-ts/TASK-*.json")
baseline = load("results/raw-snapshot-20260425-baseline/TASK-*-run-B.json")
fix = load("results/raw/TASK-*-run-B.json")
# Restrict baseline + fix to TASK-001..090 for apples-to-apples vs prev (90 tasks)
baseline_90 = [r for r in baseline if int(r["task_id"].split("-")[1]) <= 90]
fix_90 = [r for r in fix if int(r["task_id"].split("-")[1]) <= 90]

datasets = [
    stats(prev, "prev 21/04 (lean implicit)"),
    stats(baseline_90, "baseline 25/04 (lean default)"),
    stats(fix_90, "fix 25/04 (lean+nocap+min+memdisable)"),
]

hdr = f"{'dataset':<46} {'n':>3} {'score':>10} {'active_mean':>12} {'cc_mean':>10} {'tools':>6}"
print(hdr)
print("-" * len(hdr))
for d in datasets:
    if d is None:
        continue
    print(f"{d['label']:<46} {d['n']:>3} {d['score']}/{d['smax']:<7}  {d['active_mean']:>12.0f} {d['cc_mean']:>10.0f} {d['tools_total']:>6}")

# Deltas vs baseline
if datasets[0] and datasets[2]:
    p, c = datasets[0], datasets[2]
    print()
    print(f"Δ fix-vs-prev:  active {100*(c['active_mean']-p['active_mean'])/p['active_mean']:+.1f}%  "
          f"cc {100*(c['cc_mean']-p['cc_mean'])/p['cc_mean']:+.1f}%  "
          f"score {c['score']}/{c['smax']} vs {p['score']}/{p['smax']}")
if datasets[1] and datasets[2]:
    b, c = datasets[1], datasets[2]
    print(f"Δ fix-vs-base:  active {100*(c['active_mean']-b['active_mean'])/b['active_mean']:+.1f}%  "
          f"cc {100*(c['cc_mean']-b['cc_mean'])/b['cc_mean']:+.1f}%  "
          f"score {c['score']}/{c['smax']} vs {b['score']}/{b['smax']}")
