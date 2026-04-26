#!/usr/bin/env python3
"""Temporary: re-run Run B on TASK-023/024/060 with an additional
cross-validation directive appended to SYSTEM_PROMPT_TS.
Saves output to results/raw/{task}-run-B-patched.json.
"""
from __future__ import annotations
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import bench

EXTRA_DIRECTIVE = (
    "\n\nCROSS-VALIDATION (review/audit/diff tasks):\n"
    "For review, audit, and diff tasks: use Token Savior structural tools "
    "as a first-pass signal only. Always cross-validate findings with at "
    "least one native tool (Bash/grep/Read) before producing final output. "
    "Do not reproduce tool output verbatim."
)

bench.SYSTEM_PROMPT_TS = bench.SYSTEM_PROMPT_TS + EXTRA_DIRECTIVE

# Allow Read/Grep in this run so cross-validation is actually possible.
# bench.run_claude adds ["Read", "Grep", "Glob"] to --disallowedTools. We
# monkey-patch by overriding the base list via a shim.
_orig_run_claude = bench.run_claude

def run_claude_allow_native(prompt: str, run: str, extra_disallowed=None) -> dict:
    import os, subprocess, time, json as _json
    mcp_config = bench.TS_MCP_CONFIG if run == "B" else bench.EMPTY_MCP_CONFIG
    cmd = [
        "claude",
        "--permission-mode", "bypassPermissions",
        "--output-format", "stream-json",
        "--verbose",
        "--max-turns", str(bench.MAX_TURNS),
        "--strict-mcp-config",
        "--mcp-config", _json.dumps(mcp_config),
        "--no-session-persistence",
    ]
    if run == "B":
        cmd += ["--append-system-prompt", bench.SYSTEM_PROMPT_TS]
        # Intentionally do NOT disallow Read/Grep/Glob so the model can
        # cross-validate as instructed. Still honour per-task extras.
        if extra_disallowed:
            cmd += ["--disallowedTools", ",".join(extra_disallowed)]
    cmd += ["-p", prompt]

    env = os.environ.copy()
    env["IS_SANDBOX"] = "1"
    env["ENABLE_TOOL_SEARCH"] = "false"
    if run == "B":
        env["CLAUDE_PROJECT_ROOT"] = "/root/projects/tsbench"

    start = time.time()
    timed_lines = []
    stderr_chunks = []
    proc = None
    try:
        proc = subprocess.Popen(
            cmd, cwd=str(bench.CLAUDE_CWD), env=env,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            text=True, bufsize=1,
        )
        assert proc.stdout is not None
        for line in proc.stdout:
            timed_lines.append((time.time() - start, line))
            if time.time() - start > bench.TIMEOUT_SECONDS:
                proc.kill()
                raise subprocess.TimeoutExpired(cmd, bench.TIMEOUT_SECONDS)
        remaining = max(1.0, bench.TIMEOUT_SECONDS - (time.time() - start))
        proc.wait(timeout=remaining)
        if proc.stderr is not None:
            try:
                stderr_chunks.append(proc.stderr.read() or "")
            except Exception:
                pass
    except subprocess.TimeoutExpired:
        if proc is not None:
            try:
                proc.kill()
            except Exception:
                pass
        return bench._empty_metrics(bench.TIMEOUT_SECONDS, "timeout")
    wall = time.time() - start
    rc = proc.returncode if proc is not None else -1
    return bench.parse_stream_json(timed_lines, "".join(stderr_chunks), wall, rc)

bench.run_claude = run_claude_allow_native
bench.AGENTS["claude"] = run_claude_allow_native


TASKS = ["TASK-023", "TASK-024", "TASK-060"]


def run_task_patched(task_id: str) -> dict:
    out_path = bench.RAW_DIR / f"{task_id}-run-B-patched.json"

    prompt = bench.load_task_prompt(task_id)
    expected = bench.load_expected_answer(task_id)
    tasks_index = {t["id"]: t for t in bench.load_tasks_index()}
    scoring = tasks_index[task_id]["scoring"]
    extra_disallowed = tasks_index[task_id].get("disallowed_tools")

    print(f"[{task_id} | Run B-patched] starting...")
    sys.stdout.flush()
    metrics = bench.run_claude(prompt, "B", extra_disallowed=extra_disallowed)
    score, max_score = bench.score_response(scoring, expected, metrics["raw_response"])

    record = {
        "task_id": task_id,
        "run": "B-patched",
        "agent": "claude",
        "baseline": "token-savior+cross-validation",
        **metrics,
        "score": score,
        "max_score": max_score,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    bench.RAW_DIR.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(record, indent=2) + "\n")

    tb = " ".join(
        f"{k.replace('mcp__token-savior__','ts:').replace('mcp__token-savior-recall__','ts:')}×{v}"
        for k, v in record["tool_calls_breakdown"].items()
    )
    err = f" ERROR={record['error']}" if record.get("error") else ""
    print(
        f"[{task_id} | Run B-patched] done — {record['wall_time_seconds']}s | "
        f"active={record.get('active_tokens', 0)} | "
        f"tools: {tb or 'none'} | score: {record['score']}/{record['max_score']}{err}"
    )
    sys.stdout.flush()
    return record


if __name__ == "__main__":
    # Warmup once so schema-loading cost is out of task metrics.
    bench.prewarm_run_b(force=False)
    records = []
    for tid in TASKS:
        records.append(run_task_patched(tid))

    # Summary
    print("\n=== Summary ===")
    records_a = {}
    records_b = {}
    for tid in TASKS:
        p_a = bench.RAW_DIR / f"{tid}-run-A.json"
        p_b = bench.RAW_DIR / f"{tid}-run-B.json"
        if p_a.exists():
            records_a[tid] = json.loads(p_a.read_text())
        if p_b.exists():
            records_b[tid] = json.loads(p_b.read_text())

    print(f"{'Task':<12} {'A':<6} {'B (Run C)':<11} {'B-patched':<11}")
    for r in records:
        tid = r["task_id"]
        a = records_a.get(tid, {}).get("score", "-")
        b = records_b.get(tid, {}).get("score", "-")
        p = r["score"]
        print(f"{tid:<12} {str(a)+'/2':<6} {str(b)+'/2':<11} {str(p)+'/2':<11}")

    score_a = sum(records_a.get(tid, {}).get("score", 0) for tid in TASKS)
    score_b = sum(records_b.get(tid, {}).get("score", 0) for tid in TASKS)
    score_p = sum(r["score"] for r in records)
    print(f"\nTOTAL      A={score_a}/6   Run C={score_b}/6   Patched={score_p}/6")
    if score_p >= score_a:
        print("VERDICT: patched score ≥ Run A baseline → direction viable")
    else:
        print("VERDICT: patched score < Run A baseline → directive insufficient")
