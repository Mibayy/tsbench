#!/usr/bin/env python3
"""Re-score raw result files in place using the current bench.score_response.

Useful when the grader has been fixed after a run: avoids re-running the
model, just re-applies the scorer on stored raw_response + generated_code.

Skips scoring == 'llm_judge' (would trigger an external CLI call).
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from bench import score_response, load_expected_answer, load_tasks_index  # noqa: E402


def rescore_dir(d: Path, tasks: dict) -> tuple[int, int, list[str]]:
    total = changed = 0
    diffs: list[str] = []
    for p in sorted(d.glob("*.json")):
        total += 1
        raw = json.loads(p.read_text())
        tid = raw.get("task_id") or p.stem
        if tid not in tasks:
            continue
        scoring = tasks[tid].get("scoring", "contains_all")
        if scoring == "llm_judge":
            continue
        try:
            expected = load_expected_answer(tid)
        except Exception as e:
            print(f"[skip] {tid}: {e}", file=sys.stderr)
            continue
        resp = raw.get("raw_response") or ""
        gc = raw.get("generated_code") if isinstance(raw.get("generated_code"), dict) else None
        s, mx = score_response(scoring, expected, resp, gc)
        old = raw.get("score")
        if s != old or mx != raw.get("max_score") or raw.get("scoring") != scoring:
            raw["score"] = s
            raw["max_score"] = mx
            raw["scoring"] = scoring
            p.write_text(json.dumps(raw, ensure_ascii=False, indent=2))
            changed += 1
            if s != old:
                diffs.append(f"{tid}  {scoring:20s}  {old} -> {s}")
    return total, changed, diffs


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("dirs", nargs="+", help="raw-* directories to rescore")
    args = ap.parse_args()

    tasks = {t["id"]: t for t in load_tasks_index()}
    grand_total = grand_changed = 0
    for d in args.dirs:
        dp = Path(d)
        if not dp.is_dir():
            print(f"[warn] {d}: not a directory", file=sys.stderr)
            continue
        total, changed, diffs = rescore_dir(dp, tasks)
        grand_total += total
        grand_changed += changed
        print(f"\n== {d} ==")
        print(f"  files={total}  changed={changed}")
        for line in diffs:
            print(f"  {line}")
    print(f"\nTOTAL files={grand_total} changed={grand_changed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
