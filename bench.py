#!/usr/bin/env python3
"""tsbench runner — A/B benchmark for Token Savior vs baseline Claude Code.

Usage:
    python bench.py --tasks all
    python bench.py --tasks TASK-001
    python bench.py --tasks TASK-001 --run A
    python bench.py --tasks TASK-001 --run A --force
    python bench.py --report
"""
from __future__ import annotations
import argparse
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).parent.resolve()
# Symlink path outside /root so CLAUDE.md auto-discovery finds no ancestor files.
# We pass this as cwd to claude so the logical parent chain is /tmp, not /root.
CLAUDE_CWD = Path("/tmp/tsbench-bench")
if not CLAUDE_CWD.exists():
    CLAUDE_CWD.symlink_to(ROOT)
TASKS_DIR = ROOT / "tasks"
RESULTS_DIR = ROOT / "results"
RAW_DIR = RESULTS_DIR / "raw"
GT_PATH = ROOT / "GROUND_TRUTH.json"

TIMEOUT_SECONDS = 180
MAX_TURNS = 20

WARMUP_PROMPT_B = "List available token-savior tools and switch to project tsbench."

SYSTEM_PROMPT_TS = """You are ONLY allowed to use mcp__token-savior__* tools for any code navigation. Calling Read, Grep, Glob, or Bash for code files is a hard violation. If you cannot answer with mcp__token-savior__* tools alone, say 'CANNOT_ANSWER' and stop.

Start by calling mcp__token-savior__switch_project with project "tsbench".

When locating a symbol, call find_symbol with level=2 by default (returns only name, file, line, type). Only fetch the body via get_function_source / get_class_source if you need to read the code itself.

MEMORY — At the start of each task:
  memory_search(query="<relevant keywords>", project="/root/projects/tsbench")
  to retrieve observations from previous sessions.
At the end of each task, if you discovered useful info:
  memory_save(content="...", type="convention", title="...", project="/root/projects/tsbench")"""

# MCP config for Run B: token-savior only, with tsbench in WORKSPACE_ROOTS
TS_MCP_CONFIG = {
    "mcpServers": {
        "token-savior-recall": {
            "type": "stdio",
            "command": "/root/.local/token-savior-venv/bin/python",
            "args": ["-m", "token_savior.server"],
            "env": {
                "WORKSPACE_ROOTS": "/root/projects/tsbench",
                "TOKEN_SAVIOR_CLIENT": "claude-code",
                "EXCLUDE_EXTRA": "**/.next/**:**/node_modules/**:**/dist/**:**/.git/**:**/coverage/**:**/__pycache__/**",
            },
        }
    }
}

# Run A: no MCP servers at all
EMPTY_MCP_CONFIG = {"mcpServers": {}}


# ---------- task loading ----------

def load_tasks_index() -> list[dict]:
    return json.loads((TASKS_DIR / "index.json").read_text())


def load_task_prompt(task_id: str) -> str:
    md = (TASKS_DIR / f"{task_id}.md").read_text()
    # Extract the blockquote under "## Prompt"
    m = re.search(r"## Prompt.*?\n\n> (.+?)\n\n", md, re.DOTALL)
    if not m:
        raise ValueError(f"No prompt found in {task_id}.md")
    prompt = m.group(1).strip()
    return prompt + "\n\nRéponds de façon concise et précise."


def load_expected_answer(task_id: str) -> dict:
    md = (TASKS_DIR / f"{task_id}.md").read_text()
    m = re.search(r"## Réponse attendue\s*\n\n```json\n(.*?)\n```", md, re.DOTALL)
    if not m:
        return {}
    return json.loads(m.group(1))


# ---------- claude invocation ----------

def run_claude(prompt: str, run: str) -> dict:
    """Invoke claude -p with stream-json output. Returns parsed metrics."""
    mcp_config = TS_MCP_CONFIG if run == "B" else EMPTY_MCP_CONFIG
    mcp_config_str = json.dumps(mcp_config)

    cmd = [
        "claude",
        "--permission-mode", "bypassPermissions",
        "--output-format", "stream-json",
        "--verbose",
        "--max-turns", str(MAX_TURNS),
        "--strict-mcp-config",
        "--mcp-config", mcp_config_str,
        "--no-session-persistence",
    ]
    if run == "B":
        cmd += ["--append-system-prompt", SYSTEM_PROMPT_TS]
        cmd += ["--disallowedTools", "Read,Grep,Glob"]
    cmd += ["-p", prompt]

    env = os.environ.copy()
    env["IS_SANDBOX"] = "1"
    # Force Claude Code to load all MCP tool schemas eagerly. With ~100 tools
    # exposed by token-savior, the default `auto` heuristic defers them and
    # pays 1-2 ToolSearch calls per task to fetch schemas on first use. This
    # removes that overhead entirely (ToolSearch count -> 0).
    env["ENABLE_TOOL_SEARCH"] = "false"
    if run == "B":
        env["CLAUDE_PROJECT_ROOT"] = "/root/projects/tsbench"

    start = time.time()
    try:
        proc = subprocess.run(
            cmd,
            cwd=str(CLAUDE_CWD),
            env=env,
            capture_output=True,
            text=True,
            timeout=TIMEOUT_SECONDS,
        )
    except subprocess.TimeoutExpired:
        return {
            "error": "timeout",
            "wall_time_seconds": TIMEOUT_SECONDS,
            "input_tokens": 0,
            "output_tokens": 0,
            "total_tokens": 0,
            "tool_calls_count": 0,
            "tool_calls_breakdown": {},
            "ts_tool_calls_count": 0,
            "raw_response": "",
        }
    wall = time.time() - start

    return parse_stream_json(proc.stdout, proc.stderr, wall, proc.returncode)


def parse_stream_json(stdout: str, stderr: str, wall: float, rc: int) -> dict:
    """Parse stream-json output into metrics."""
    input_tokens = 0
    output_tokens = 0
    cache_creation = 0
    cache_read = 0
    tool_breakdown: dict[str, int] = {}
    raw_response = ""
    error: str | None = None
    final_result_seen = False
    turns_count = 0
    tool_use_name_by_id: dict[str, str] = {}
    tool_calls_detail: list[dict] = []

    def _result_chars(content) -> int:
        if content is None:
            return 0
        if isinstance(content, str):
            return len(content)
        if isinstance(content, list):
            total = 0
            for b in content:
                if isinstance(b, dict):
                    if isinstance(b.get("text"), str):
                        total += len(b["text"])
                    elif isinstance(b.get("content"), str):
                        total += len(b["content"])
                    else:
                        total += len(json.dumps(b, ensure_ascii=False))
                else:
                    total += len(str(b))
            return total
        return len(json.dumps(content, ensure_ascii=False))

    for line in stdout.splitlines():
        line = line.strip()
        if not line or not line.startswith("{"):
            continue
        try:
            ev = json.loads(line)
        except json.JSONDecodeError:
            continue
        et = ev.get("type")
        if et == "assistant":
            turns_count += 1
            msg = ev.get("message", {})
            for block in msg.get("content", []):
                if block.get("type") == "tool_use":
                    name = block.get("name", "unknown")
                    tid = block.get("id")
                    tool_breakdown[name] = tool_breakdown.get(name, 0) + 1
                    if tid:
                        tool_use_name_by_id[tid] = name
        elif et == "user":
            msg = ev.get("message", {})
            content = msg.get("content", [])
            if isinstance(content, list):
                for block in content:
                    if isinstance(block, dict) and block.get("type") == "tool_result":
                        tid = block.get("tool_use_id")
                        chars = _result_chars(block.get("content"))
                        tool_calls_detail.append({
                            "tool": tool_use_name_by_id.get(tid, "unknown"),
                            "result_chars": chars,
                            "is_error": bool(block.get("is_error")),
                        })
        elif et == "result":
            final_result_seen = True
            raw_response = ev.get("result", "") or ""
            usage = ev.get("usage", {}) or {}
            input_tokens = usage.get("input_tokens", 0) or 0
            output_tokens = usage.get("output_tokens", 0) or 0
            cache_creation = usage.get("cache_creation_input_tokens", 0) or 0
            cache_read = usage.get("cache_read_input_tokens", 0) or 0
            if ev.get("is_error"):
                error = ev.get("subtype") or "api_error"

    if not final_result_seen:
        error = error or f"no_result_event (rc={rc})"
        if stderr:
            error += f" | stderr: {stderr[:300]}"

    total = input_tokens + output_tokens + cache_creation + cache_read
    active_tokens = input_tokens + output_tokens + cache_creation
    tool_calls_count = sum(tool_breakdown.values())
    total_context_chars_injected = sum(d["result_chars"] for d in tool_calls_detail)
    ts_tool_calls_count = sum(
        v for k, v in tool_breakdown.items() if k.startswith("mcp__token-savior__")
    )

    return {
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "cache_creation_input_tokens": cache_creation,
        "cache_read_input_tokens": cache_read,
        "total_tokens": total,
        "active_tokens": active_tokens,
        "turns_count": turns_count,
        "tool_calls_count": tool_calls_count,
        "tool_calls_breakdown": tool_breakdown,
        "tool_calls_detail": tool_calls_detail,
        "total_context_chars_injected": total_context_chars_injected,
        "ts_tool_calls_count": ts_tool_calls_count,
        "wall_time_seconds": round(wall, 2),
        "raw_response": raw_response,
        "error": error,
    }


# ---------- scoring ----------

def extract_files(text: str) -> set[str]:
    """Extract file-like paths from response text."""
    out = set()
    # file with optional line: path/to/file.ext(:line)
    for m in re.finditer(r"[\w\-/\.]+\.(?:py|ts|tsx|js|jsx|json|md|yml|yaml|env|Dockerfile|toml)(?::\d+)?", text):
        path = m.group(0).split(":")[0]
        out.add(path)
    return out


def extract_symbols(text: str) -> set[str]:
    """Extract identifier-like tokens (function/class names)."""
    out = set()
    for m in re.finditer(r"`([A-Za-z_][A-Za-z0-9_]*)`", text):
        out.add(m.group(1))
    for m in re.finditer(r"\b([a-z_][a-z0-9_]{3,})\(", text):
        out.add(m.group(1))
    return out


def f1(expected: set, got: set) -> float:
    if not expected and not got:
        return 1.0
    if not expected or not got:
        return 0.0
    tp = len(expected & got)
    if tp == 0:
        return 0.0
    precision = tp / len(got)
    recall = tp / len(expected)
    return 2 * precision * recall / (precision + recall)


def score_response(scoring: str, expected: dict, response: str) -> tuple[int, int]:
    """Return (score, max_score)."""
    max_score = 2
    if not response:
        return 0, max_score
    text = response.lower()

    if scoring == "exact_match":
        # Look for file + symbol (+ optionally line)
        exp_file = (expected.get("file") or "").lower()
        exp_symbol = (expected.get("symbol") or expected.get("type") or "").lower()
        has_file = exp_file and exp_file in text
        has_symbol = exp_symbol and exp_symbol in text
        if has_file and has_symbol:
            return 2, max_score
        if has_file or has_symbol:
            return 1, max_score
        return 0, max_score

    if scoring in ("list_f1", "set_match_strict", "set_match_loose"):
        exp_list = (
            expected.get("expected_files")
            or expected.get("expected_breaks")
            or expected.get("files")
            or expected.get("items")
            or expected.get("chain")
            or []
        )
        if not exp_list:
            return 0, max_score
        exp_set = {str(x).lower() for x in exp_list}
        got_files = {f.lower() for f in extract_files(response)}
        got_symbols = {s.lower() for s in extract_symbols(response)}
        got = got_files | got_symbols | {w.lower() for w in response.split()}
        hits = sum(1 for e in exp_set if any(e in g or g in e for g in got) or e in text)
        if hits == 0:
            return 0, max_score
        recall = hits / len(exp_set)
        # Precision hard to measure from free text; approximate with recall
        if recall >= 0.95:
            return 2, max_score
        if recall >= 0.5:
            return 1, max_score
        return 0, max_score

    if scoring in ("contains_all", "diff_review", "chain_match", "boolean_with_evidence", "free_form_rubric", "edit_quality", "impact_set"):
        # Collect candidate expected strings from the dict
        candidates: list[str] = []
        for v in expected.values():
            if isinstance(v, str):
                candidates.append(v)
            elif isinstance(v, list):
                candidates.extend(str(x) for x in v)
        if not candidates:
            return 0, max_score
        hits = sum(1 for c in candidates if c.lower() in text)
        ratio = hits / len(candidates)
        if ratio >= 0.9:
            return 2, max_score
        if ratio >= 0.5:
            return 1, max_score
        return 0, max_score

    return 0, max_score


# ---------- checkpoint + runner ----------

def result_path(task_id: str, run: str) -> Path:
    return RAW_DIR / f"{task_id}-run-{run}.json"


WARMUP_PATH = None  # set lazily to avoid module-load ordering issues


def prewarm_run_b(force: bool = False) -> None:
    """Pay the ToolSearch + MCP schema-loading cost once, outside task metrics.

    Subsequent Run B tasks hit the Anthropic prompt cache for the shared prefix
    (system prompt + MCP config), so they don't re-pay schema load each time.
    """
    path = RESULTS_DIR / "warmup-run-B.json"
    if path.exists() and not force:
        print("[Run B | warmup] skip (checkpoint exists)")
        sys.stdout.flush()
        return
    print("[Run B | warmup] starting...")
    sys.stdout.flush()
    metrics = run_claude(WARMUP_PROMPT_B, "B")
    record = {
        "kind": "warmup",
        "run": "B",
        **metrics,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(record, indent=2) + "\n")
    tb = " ".join(
        f"{k.replace('mcp__token-savior__','ts:')}×{v}"
        for k, v in record["tool_calls_breakdown"].items()
    )
    err = f" ERROR={record['error']}" if record.get("error") else ""
    print(
        f"[Run B | warmup] done — {record['wall_time_seconds']}s | "
        f"tokens: {record['input_tokens']} in + {record['output_tokens']} out "
        f"(cache {record['cache_creation_input_tokens']}c/{record['cache_read_input_tokens']}r) | "
        f"tools: {tb or 'none'}{err}"
    )
    sys.stdout.flush()


def run_task(task_id: str, run: str, force: bool = False) -> dict | None:
    out_path = result_path(task_id, run)
    if out_path.exists() and not force:
        print(f"[{task_id} | Run {run}] skip (checkpoint exists)")
        return json.loads(out_path.read_text())

    prompt = load_task_prompt(task_id)
    expected = load_expected_answer(task_id)
    tasks_index = {t["id"]: t for t in load_tasks_index()}
    scoring = tasks_index[task_id]["scoring"]

    print(f"[{task_id} | Run {run}] starting...")
    sys.stdout.flush()
    metrics = run_claude(prompt, run)

    score, max_score = score_response(scoring, expected, metrics["raw_response"])

    record = {
        "task_id": task_id,
        "run": run,
        "baseline": "plain" if run == "A" else "token-savior",
        **metrics,
        "score": score,
        "max_score": max_score,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(record, indent=2) + "\n")

    tb = " ".join(f"{k.replace('mcp__token-savior__','ts:')}×{v}" for k, v in record["tool_calls_breakdown"].items())
    err = f" ERROR={record['error']}" if record.get("error") else ""
    print(
        f"[{task_id} | Run {run}] done — {record['wall_time_seconds']}s | "
        f"tokens: {record['input_tokens']} in + {record['output_tokens']} out "
        f"(cache {record['cache_creation_input_tokens']}c/{record['cache_read_input_tokens']}r) | "
        f"tools: {tb or 'none'} | score: {record['score']}/{record['max_score']}{err}"
    )
    sys.stdout.flush()
    return record


# ---------- report ----------

def _active(r: dict) -> int:
    if "active_tokens" in r:
        return r["active_tokens"]
    return (
        (r.get("input_tokens") or 0)
        + (r.get("output_tokens") or 0)
        + (r.get("cache_creation_input_tokens") or 0)
    )


def _turns(r: dict) -> int:
    if "turns_count" in r:
        return r["turns_count"]
    # Fallback for legacy records: approx = 1 (final msg) + 1 per tool call round.
    return 1 + (r.get("tool_calls_count") or 0)


def _chars(r: dict) -> int | None:
    v = r.get("total_context_chars_injected")
    return v if isinstance(v, int) else None


def generate_report() -> None:
    records_a: dict[str, dict] = {}
    records_b: dict[str, dict] = {}
    for p in sorted(RAW_DIR.glob("*.json")):
        r = json.loads(p.read_text())
        (records_a if r["run"] == "A" else records_b)[r["task_id"]] = r

    tasks_index = {t["id"]: t for t in load_tasks_index()}
    task_ids = sorted(set(records_a) | set(records_b))

    lines: list[str] = ["# tsbench — RESULTS\n"]
    lines.append(f"_Generated {datetime.now(timezone.utc).isoformat()}_\n")

    # Executive summary
    pairs = [(records_a.get(t), records_b.get(t)) for t in task_ids if records_a.get(t) and records_b.get(t)]
    if pairs:
        act_a = sum(_active(p[0]) for p in pairs)
        act_b = sum(_active(p[1]) for p in pairs)
        reduction = (act_a - act_b) / act_a * 100 if act_a else 0
        turns_a = sum(_turns(p[0]) for p in pairs)
        turns_b = sum(_turns(p[1]) for p in pairs)
        score_a = sum(p[0]["score"] for p in pairs)
        score_b = sum(p[1]["score"] for p in pairs)
        max_score = sum(p[0]["max_score"] for p in pairs)
        wins_b = sum(1 for p in pairs if p[1]["score"] > p[0]["score"])
        wins_a = sum(1 for p in pairs if p[0]["score"] > p[1]["score"])
        ties = len(pairs) - wins_a - wins_b
        lines.append("## 1. Résumé exécutif\n")
        lines.append("_Métrique principale : `active_tokens` = input + output + cache_creation (cache_read exclu — contexte réutilisé, proxy du coût quota abonnement)._\n")
        lines.append(f"- **Tâches appariées** : {len(pairs)}")
        lines.append(f"- **Réduction active_tokens A→B** : {reduction:.1f}% ({act_a:,} → {act_b:,})")
        lines.append(f"- **Turns cumulés** : A={turns_a} · B={turns_b}")
        lines.append(f"- **Score global A** : {score_a}/{max_score} ({score_a/max_score*100:.0f}%)")
        lines.append(f"- **Score global B** : {score_b}/{max_score} ({score_b/max_score*100:.0f}%)")
        lines.append(f"- **Token Savior** : gagne {wins_b}, ex æquo {ties}, perd {wins_a}\n")

    # Main table
    lines.append("## 2. Tableau principal\n")
    lines.append("| Task | Catégorie | Active A | Active B | ΔActive | Chars A | Chars B | ΔChars | Score A | Score B |")
    lines.append("|---|---|---:|---:|---:|---:|---:|---:|---:|---:|")
    for tid in task_ids:
        a = records_a.get(tid)
        b = records_b.get(tid)
        cat = tasks_index.get(tid, {}).get("category", "?")
        ta = _active(a) if a else None
        tb = _active(b) if b else None
        red_act = f"{(ta-tb)/ta*100:+.0f}%" if ta and tb else "—"
        ca = _chars(a) if a else None
        cb = _chars(b) if b else None
        if ca is not None and cb is not None and ca > 0:
            red_chr = f"{(ca-cb)/ca*100:+.0f}%"
        elif ca is not None and cb is not None:
            red_chr = "—"
        else:
            red_chr = "—"
        sa = f"{a['score']}/{a['max_score']}" if a else "—"
        sb = f"{b['score']}/{b['max_score']}" if b else "—"
        ca_s = f"{ca:,}" if ca is not None else "—"
        cb_s = f"{cb:,}" if cb is not None else "—"
        lines.append(f"| {tid} | {cat} | {ta or '—'} | {tb or '—'} | {red_act} | {ca_s} | {cb_s} | {red_chr} | {sa} | {sb} |")

    # Per-category averages
    lines.append("\n## 3. Moyennes par catégorie\n")
    cats: dict[str, list[tuple[dict, dict]]] = {}
    for a, b in pairs:
        c = tasks_index.get(a["task_id"], {}).get("category", "?")
        cats.setdefault(c, []).append((a, b))
    lines.append("| Catégorie | N | Active A moy | Active B moy | Réduction | Turns A moy | Turns B moy | Score A moy | Score B moy |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|")
    for c, lst in sorted(cats.items()):
        n = len(lst)
        ta = sum(_active(x[0]) for x in lst) / n
        tb = sum(_active(x[1]) for x in lst) / n
        red = (ta - tb) / ta * 100 if ta else 0
        ura = sum(_turns(x[0]) for x in lst) / n
        urb = sum(_turns(x[1]) for x in lst) / n
        sa = sum(x[0]["score"] for x in lst) / n
        sb = sum(x[1]["score"] for x in lst) / n
        lines.append(f"| {c} | {n} | {ta:,.0f} | {tb:,.0f} | {red:+.0f}% | {ura:.1f} | {urb:.1f} | {sa:.2f} | {sb:.2f} |")

    # Context-injection winners/losers and break-even analysis
    lines.append("\n## 3bis. Analyse chars_injected (ce que TS prétend économiser)\n")
    char_pairs = [(a, b) for a, b in pairs if _chars(a) is not None and _chars(b) is not None]
    if char_pairs:
        wins_chars = [(a, b) for a, b in char_pairs if _chars(b) < _chars(a)]
        losses_chars = [(a, b) for a, b in char_pairs if _chars(b) > _chars(a)]
        ties_chars = [(a, b) for a, b in char_pairs if _chars(b) == _chars(a)]
        total_ca = sum(_chars(a) for a, b in char_pairs)
        total_cb = sum(_chars(b) for a, b in char_pairs)
        lines.append(f"- **Pairs mesurés** : {len(char_pairs)}")
        lines.append(f"- **Chars injectés cumulés** : A={total_ca:,} · B={total_cb:,} · Δ={((total_ca-total_cb)/total_ca*100) if total_ca else 0:+.0f}%")
        lines.append(f"- **TS gagne sur chars** : {len(wins_chars)}/{len(char_pairs)}")
        lines.append(f"- **TS perd sur chars** : {len(losses_chars)}/{len(char_pairs)}")
        lines.append(f"- **Ex æquo** : {len(ties_chars)}/{len(char_pairs)}\n")

        lines.append("### Tâches où TS gagne sur chars_injected\n")
        if not wins_chars:
            lines.append("_Aucune._\n")
        else:
            for a, b in sorted(wins_chars, key=lambda x: _chars(x[0]) - _chars(x[1]), reverse=True):
                ca, cb = _chars(a), _chars(b)
                aa, ab = _active(a), _active(b)
                lines.append(f"- **{a['task_id']}** — chars {ca:,}→{cb:,} ({(cb-ca)/ca*100:+.0f}%) | active {aa:,}→{ab:,} ({(ab-aa)/aa*100:+.0f}%)")
            lines.append("")

        lines.append("### Tâches où TS perd sur chars_injected\n")
        if not losses_chars:
            lines.append("_Aucune._\n")
        else:
            for a, b in sorted(losses_chars, key=lambda x: _chars(x[1]) - _chars(x[0]), reverse=True):
                ca, cb = _chars(a), _chars(b)
                aa, ab = _active(a), _active(b)
                lines.append(f"- **{a['task_id']}** — chars {ca:,}→{cb:,} ({(cb-ca)/ca*100:+.0f}%) | active {aa:,}→{ab:,} ({(ab-aa)/aa*100:+.0f}%)")
            lines.append("")

        lines.append("### Break-even analysis\n")
        lines.append("_Coût fixe B = active_tokens B − chars_injected B (baseline TS : system prompt, schémas ToolSearch). Gain chars = chars_A − chars_B. TS rentable sur active_tokens si : (active_A − active_B) ≥ 0, i.e. le gain chars_injected doit couvrir le surcoût baseline._\n")
        overhead_samples = [(_active(b) - _active(a)) for a, b in char_pairs]
        avg_overhead = sum(overhead_samples) / len(overhead_samples) if overhead_samples else 0
        lines.append(f"- **Surcoût moyen active_tokens B − A** : {avg_overhead:+,.0f} tokens / tâche")
        lines.append(f"- **Cas où B ≤ A sur active** : {sum(1 for o in overhead_samples if o <= 0)}/{len(overhead_samples)}")
        gain_losses = [((_chars(a) - _chars(b)), (_active(b) - _active(a)), a['task_id']) for a, b in char_pairs]
        gain_losses.sort(key=lambda x: x[0], reverse=True)
        lines.append("\n| Task | Gain chars (A−B) | Surcoût active (B−A) |")
        lines.append("|---|---:|---:|")
        for gc, oa, tid in gain_losses:
            lines.append(f"| {tid} | {gc:+,} | {oa:+,} |")
        lines.append("")

    # Where TS loses
    lines.append("\n## 4. Tâches où Token Savior perd\n")
    losers = [(a, b) for a, b in pairs if _active(b) > _active(a) or a["score"] > b["score"]]
    if not losers:
        lines.append("_Aucune._")
    else:
        for a, b in losers:
            lines.append(f"- **{a['task_id']}** — active {_active(a):,} → {_active(b):,} | score {a['score']}→{b['score']}")

    # Impossible without TS
    lines.append("\n## 5. Tâches impossibles sans Token Savior\n")
    impossible = [(a, b) for a, b in pairs if a["score"] == 0 and b["score"] > 0]
    if not impossible:
        lines.append("_Aucune._")
    else:
        for a, b in impossible:
            lines.append(f"- **{a['task_id']}** — score A=0, score B={b['score']}/{b['max_score']}")

    # Tool distribution
    lines.append("\n## 6. Distribution des tool calls\n")
    def top_tools(records: dict[str, dict]) -> list[tuple[str, int]]:
        agg: dict[str, int] = {}
        for r in records.values():
            for k, v in r.get("tool_calls_breakdown", {}).items():
                agg[k] = agg.get(k, 0) + v
        return sorted(agg.items(), key=lambda x: -x[1])
    top_a = top_tools(records_a)
    top_b = top_tools(records_b)
    lines.append("**Run A (plain)** — top 5 :")
    for name, n in top_a[:5]:
        lines.append(f"- `{name}` : {n}")
    total_b = sum(n for _, n in top_b) or 1
    ts_b = sum(n for name, n in top_b if name.startswith("mcp__token-savior__"))
    lines.append(f"\n**Run B (token-savior)** — top 5 (TS/total = {ts_b}/{total_b} = {ts_b/total_b*100:.0f}%) :")
    for name, n in top_b[:5]:
        lines.append(f"- `{name}` : {n}")

    # Speed analysis
    lines.append("\n## 7. Rapidité\n")
    speed_pairs = [(a, b) for a, b in pairs if a.get("wall_time_seconds") and b.get("wall_time_seconds")]
    if speed_pairs:
        wa = [p[0]["wall_time_seconds"] for p in speed_pairs]
        wb = [p[1]["wall_time_seconds"] for p in speed_pairs]
        total_a, total_b = sum(wa), sum(wb)
        avg_a, avg_b = total_a / len(wa), total_b / len(wb)
        delta_total = (total_b - total_a) / total_a * 100 if total_a else 0
        lines.append(f"- **Wall time moyen / tâche** : A={avg_a:.1f}s · B={avg_b:.1f}s ({delta_total:+.0f}%)")
        lines.append(f"- **Wall time total (14 tâches)** : A={total_a:.1f}s · B={total_b:.1f}s ({delta_total:+.0f}%)\n")

        lines.append("### Par catégorie\n")
        lines.append("| Catégorie | N | Wall A moy | Wall B moy | Δ | Wall A total | Wall B total |")
        lines.append("|---|---:|---:|---:|---:|---:|---:|")
        speed_cats: dict[str, list[tuple[dict, dict]]] = {}
        for a, b in speed_pairs:
            c = tasks_index.get(a["task_id"], {}).get("category", "?")
            speed_cats.setdefault(c, []).append((a, b))
        for c, lst in sorted(speed_cats.items()):
            n = len(lst)
            ta = sum(x[0]["wall_time_seconds"] for x in lst)
            tb = sum(x[1]["wall_time_seconds"] for x in lst)
            ma, mb = ta / n, tb / n
            d = (tb - ta) / ta * 100 if ta else 0
            lines.append(f"| {c} | {n} | {ma:.1f}s | {mb:.1f}s | {d:+.0f}% | {ta:.1f}s | {tb:.1f}s |")

        faster = []
        slower = []
        for a, b in speed_pairs:
            ratio = (b["wall_time_seconds"] - a["wall_time_seconds"]) / a["wall_time_seconds"] * 100 if a["wall_time_seconds"] else 0
            if ratio <= -20:
                faster.append((a, b, ratio))
            elif ratio >= 20:
                slower.append((a, b, ratio))

        lines.append("\n### Tâches où TS est significativement plus rapide (>20%)\n")
        if not faster:
            lines.append("_Aucune._")
        else:
            for a, b, r in sorted(faster, key=lambda x: x[2]):
                lines.append(f"- **{a['task_id']}** — {a['wall_time_seconds']:.1f}s → {b['wall_time_seconds']:.1f}s ({r:+.0f}%)")

        lines.append("\n### Tâches où TS est significativement plus lent (>20%)\n")
        if not slower:
            lines.append("_Aucune._")
        else:
            for a, b, r in sorted(slower, key=lambda x: -x[2]):
                lines.append(f"- **{a['task_id']}** — {a['wall_time_seconds']:.1f}s → {b['wall_time_seconds']:.1f}s ({r:+.0f}%)")
        lines.append("")

    lines.append("\n## 8. Données brutes\n")
    lines.append("Voir [`results/raw/`](./raw/) pour les JSON par run.")

    out = RESULTS_DIR / "RESULTS.md"
    out.write_text("\n".join(lines) + "\n")
    print(f"Report written: {out}")


# ---------- main ----------

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tasks", default=None, help="'all' or a task ID like TASK-001")
    ap.add_argument("--run", choices=["A", "B", "both"], default="both")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--report", action="store_true")
    args = ap.parse_args()

    if args.report:
        generate_report()
        return 0

    if not args.tasks:
        ap.error("--tasks is required (or use --report)")

    all_tasks = [t["id"] for t in load_tasks_index()]
    if args.tasks == "all":
        targets = all_tasks
    else:
        targets = [t.strip() for t in args.tasks.split(",") if t.strip()]
    runs = ["A", "B"] if args.run == "both" else [args.run]

    if "B" in runs:
        prewarm_run_b(force=args.force)

    for tid in targets:
        for run in runs:
            try:
                run_task(tid, run, force=args.force)
            except Exception as e:
                print(f"[{tid} | Run {run}] CRASHED: {e}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
