#!/usr/bin/env python3
"""Consolidate per-config raw results into a single results/matrix.json.

Reads `results/raw-{config_id}/*.json` for each known config and emits
`results/matrix.json` following docs/matrix-schema.md.

Usage:
    python3 scripts/build_matrix.py
    python3 scripts/build_matrix.py --out results/matrix.json
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RESULTS_DIR = ROOT / "results"
TASKS_DIR = ROOT / "tasks"
TASKS_INDEX = TASKS_DIR / "index.json"


def _extract_prompt(tid: str) -> str | None:
    """Pull the prompt line out of tasks/TASK-XXX.md (blockquote after 'Prompt')."""
    p = TASKS_DIR / f"{tid}.md"
    if not p.is_file():
        return None
    try:
        text = p.read_text()
    except OSError:
        return None
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if line.lstrip().startswith("## Prompt"):
            for j in range(i + 1, min(i + 20, len(lines))):
                stripped = lines[j].lstrip()
                if stripped.startswith("> "):
                    return stripped[2:].strip()
            break
    return None

CONFIGS = [
    {"id": "opus-base",   "model": "claude-opus-4-7",           "mode": "base", "run_letter": "A"},
    {"id": "opus-ts",     "model": "claude-opus-4-7",           "mode": "ts",   "run_letter": "B"},
    {"id": "sonnet-base", "model": "claude-sonnet-4-6",         "mode": "base", "run_letter": "A"},
    {"id": "sonnet-ts",   "model": "claude-sonnet-4-6",         "mode": "ts",   "run_letter": "B"},
    {"id": "haiku-base",  "model": "claude-haiku-4-5-20251001", "mode": "base", "run_letter": "A"},
    {"id": "haiku-ts",    "model": "claude-haiku-4-5-20251001", "mode": "ts",   "run_letter": "B"},
]


def load_tasks_index() -> dict[str, dict]:
    """Return {task_id: task_meta}. Handles the blank-line-delimited JSON array."""
    text = TASKS_INDEX.read_text()
    clean = "\n".join(line for line in text.splitlines() if line.strip())
    data = json.loads(clean) if clean.startswith("[") else json.loads(text)
    return {t["id"]: t for t in data}


def extract_task_result(raw: dict) -> dict:
    return {
        "active_tokens":     raw.get("active_tokens"),
        "total_tokens":      raw.get("total_tokens"),
        "turns":             raw.get("turns_count"),
        "tool_calls":        raw.get("tool_calls_count"),
        "wall_time_seconds": raw.get("wall_time_seconds"),
        "score":             raw.get("score"),
        "max_score":         raw.get("max_score"),
        "error":             raw.get("error"),
        "context_chars":     raw.get("total_context_chars_injected"),
    }


def load_config_results(config_id: str) -> dict[str, dict]:
    """Return {task_id: per_task_result} for a given config, or {} if missing."""
    cdir = RESULTS_DIR / f"raw-{config_id}"
    if not cdir.is_dir():
        return {}
    out: dict[str, dict] = {}
    for p in sorted(cdir.glob("*.json")):
        try:
            raw = json.loads(p.read_text())
        except (OSError, json.JSONDecodeError) as e:
            print(f"[warn] skip {p}: {e}", file=sys.stderr)
            continue
        tid = raw.get("task_id") or p.stem.split("-run-")[0]
        out[tid] = extract_task_result(raw)
    return out


def config_summary(results: dict[str, dict], tasks_index: dict[str, dict] | None = None) -> dict:
    present = [(tid, r) for tid, r in results.items() if r is not None and r.get("active_tokens") is not None]
    n = len(present)
    if n == 0:
        return {
            "n_tasks": 0, "active_tokens_total": 0, "active_tokens_mean": 0,
            "turns_total": 0, "score_total": 0, "score_max_total": 0,
            "score_pct": 0.0, "wall_time_total": 0.0,
            "context_chars_total": 0,
            "by_category": {},
        }
    act_total = sum((r["active_tokens"] or 0) for _, r in present)
    turns_total = sum((r["turns"] or 0) for _, r in present)
    score_total = sum((r["score"] or 0) for _, r in present)
    smax_total = sum((r["max_score"] or 0) for _, r in present)
    wall_total = sum((r["wall_time_seconds"] or 0) for _, r in present)
    chars_total = sum((r.get("context_chars") or 0) for _, r in present)

    by_cat: dict[str, dict] = {}
    if tasks_index:
        for tid, r in present:
            cat = (tasks_index.get(tid) or {}).get("category") or "other"
            acc = by_cat.setdefault(cat, {"n": 0, "score": 0, "max": 0, "chars": 0, "active": 0, "wall": 0.0})
            acc["n"] += 1
            acc["score"] += r.get("score") or 0
            acc["max"] += r.get("max_score") or 0
            acc["chars"] += r.get("context_chars") or 0
            acc["active"] += r.get("active_tokens") or 0
            acc["wall"] += r.get("wall_time_seconds") or 0
        for cat, acc in by_cat.items():
            acc["pct"] = round(acc["score"] / acc["max"] * 100, 1) if acc["max"] else 0.0
            acc["wall"] = round(acc["wall"], 1)

    return {
        "n_tasks": n,
        "active_tokens_total": act_total,
        "active_tokens_mean": round(act_total / n, 1),
        "turns_total": turns_total,
        "score_total": score_total,
        "score_max_total": smax_total,
        "score_pct": round(score_total / smax_total * 100, 1) if smax_total else 0.0,
        "wall_time_total": round(wall_total, 1),
        "context_chars_total": chars_total,
        "by_category": by_cat,
    }


def pair_summary(
    base_id: str, ts_id: str,
    base_res: dict[str, dict], ts_res: dict[str, dict],
) -> dict:
    common = sorted(set(base_res) & set(ts_res))
    paired = [
        (base_res[t], ts_res[t])
        for t in common
        if base_res[t].get("active_tokens") is not None
        and ts_res[t].get("active_tokens") is not None
    ]
    if not paired:
        return {"base": base_id, "ts": ts_id, "n_paired": 0}
    act_a = sum(a["active_tokens"] for a, _ in paired)
    act_b = sum(b["active_tokens"] for _, b in paired)
    wall_a = sum((a.get("wall_time_seconds") or 0) for a, _ in paired)
    wall_b = sum((b.get("wall_time_seconds") or 0) for _, b in paired)
    chars_a = sum((a.get("context_chars") or 0) for a, _ in paired)
    chars_b = sum((b.get("context_chars") or 0) for _, b in paired)
    score_a = sum((a["score"] or 0) for a, _ in paired)
    score_b = sum((b["score"] or 0) for _, b in paired)
    smax = sum((a.get("max_score") or 0) for a, _ in paired)
    wins_ts = sum(1 for a, b in paired if (b["score"] or 0) > (a["score"] or 0))
    wins_base = sum(1 for a, b in paired if (a["score"] or 0) > (b["score"] or 0))
    ties = len(paired) - wins_ts - wins_base

    def _pct_drop(a: float, b: float) -> float:
        return round((a - b) / a * 100, 1) if a else 0.0

    return {
        "base": base_id,
        "ts": ts_id,
        "n_paired": len(paired),
        "reduction_active_pct": _pct_drop(act_a, act_b),
        "reduction_wall_pct":   _pct_drop(wall_a, wall_b),
        "reduction_chars_pct":  _pct_drop(chars_a, chars_b),
        "accuracy_base_pct":    round(score_a / smax * 100, 1) if smax else 0.0,
        "accuracy_ts_pct":      round(score_b / smax * 100, 1) if smax else 0.0,
        "accuracy_delta_pp":    round((score_b - score_a) / smax * 100, 1) if smax else 0.0,
        "active_tokens_base":   act_a,
        "active_tokens_ts":     act_b,
        "wall_seconds_base":    round(wall_a, 1),
        "wall_seconds_ts":      round(wall_b, 1),
        "context_chars_base":   chars_a,
        "context_chars_ts":     chars_b,
        "score_base":           score_a,
        "score_ts":             score_b,
        "score_max":            smax,
        "delta_score":          score_b - score_a,
        "wins_ts":              wins_ts,
        "ties":                 ties,
        "wins_base":            wins_base,
    }


def build_matrix() -> dict:
    tasks_index = load_tasks_index()
    per_config: dict[str, dict[str, dict]] = {
        c["id"]: {tid: r for tid, r in load_config_results(c["id"]).items() if tid in tasks_index}
        for c in CONFIGS
    }

    # tasks/index.json is the source of truth (90 tasks, non-contiguous IDs).
    # Raw dirs may contain results for dropped tasks - those are ignored.
    all_task_ids = sorted(tasks_index)

    tasks_out: dict[str, dict] = {}
    for tid in all_task_ids:
        meta = tasks_index.get(tid, {})
        row = {
            "category":   meta.get("category"),
            "difficulty": meta.get("difficulty"),
            "scoring":    meta.get("scoring"),
            "slug":       meta.get("slug"),
            "prompt":     _extract_prompt(tid),
            "results": {cid: per_config[cid].get(tid) for cid in per_config},
        }
        tasks_out[tid] = row

    configs_out = []
    for c in CONFIGS:
        configs_out.append({
            **c,
            "source_dir": f"raw-{c['id']}",
            "tasks_covered": len(per_config[c["id"]]),
        })

    summary_out = {cid: config_summary(per_config[cid], tasks_index) for cid in per_config}

    pairs_out = {}
    for model_short in ("opus", "sonnet", "haiku"):
        base_id = f"{model_short}-base"
        ts_id = f"{model_short}-ts"
        pairs_out[model_short] = pair_summary(
            base_id, ts_id, per_config[base_id], per_config[ts_id]
        )

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "task_count": len(all_task_ids),
        "configs": configs_out,
        "tasks": tasks_out,
        "summary": summary_out,
        "pairs": pairs_out,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(RESULTS_DIR / "matrix.json"))
    args = ap.parse_args()

    matrix = build_matrix()
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(matrix, ensure_ascii=False, indent=2))

    covered = {c["id"]: c["tasks_covered"] for c in matrix["configs"]}
    print(f"[build_matrix] wrote {out_path}")
    print(f"[build_matrix] task_count={matrix['task_count']}")
    for cid, n in covered.items():
        print(f"  {cid:12s} : {n:3d} tasks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
