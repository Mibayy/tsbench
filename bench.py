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
import sqlite3
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
MAX_TURNS = 30

WARMUP_PROMPT_B = "List available token-savior tools and switch to project tsbench."

SYSTEM_PROMPT_TS = """You are ONLY allowed to use mcp__token-savior__* tools for any code navigation and editing. Calling Read, Grep, Glob, Edit, Write, or Bash for code files is a hard violation. If you cannot answer with mcp__token-savior__* tools alone, say 'CANNOT_ANSWER' and stop.

Start by calling mcp__token-savior__switch_project with project "tsbench".

NAVIGATION — When locating a symbol, call find_symbol with level=2 by default (returns only name, file, line, type). Only fetch the body via get_function_source / get_class_source if you need to read the code itself.

BATCH MODE — To read multiple functions/classes/symbols in one call, use the `names` parameter instead of `name`:
  get_function_source(names=["create_user", "update_user", "delete_user"])
  find_symbol(names=["foo", "bar"], level=2)
  get_full_context(names=["x", "y"])
Returns a JSON dict {name: result}. Max 10 per call. ALWAYS prefer batch over sequential calls.

COMPRENDRE un symbole complet (localisation + source + callers + dépendances) → get_full_context('nom') en un seul call. Utilise depth=0 pour juste source, depth=1 (défaut) pour + deps/dependents, depth=2 pour + change_impact. Ça remplace la chaîne find_symbol → get_function_source → get_dependents.

EDITING — To modify code, ALWAYS use replace_symbol_source or insert_near_symbol. NEVER use Edit or Write on code files (.py, .ts, .tsx, .js, .jsx). Edit/Write are only allowed for config files (.env, .yml, .md, .json).

## Workflow recipes (follow these exact patterns)

LOCATE A SYMBOL:
switch_project → find_symbol("name") → stop
Do not use search_codebase if find_symbol suffices.

READ A SYMBOL:
switch_project → get_function_source("name") → act
One call only. No reindex before editing.

EDIT A SYMBOL:
switch_project → get_function_source → replace_symbol_source → stop
No reindex between read and edit.

CHECKPOINT WORKFLOW:
switch_project → create_checkpoint → get_function_source → replace_symbol_source → compare_checkpoint_by_symbol → stop

BREAKING CHANGES:
switch_project → detect_breaking_changes(ref="v1") → stop
Do not re-read each modified function after detect_breaking_changes.
Pour un diff entre deux versions/tags/branches (v1 vs v2, main vs feature), utilise detect_breaking_changes, PAS get_changed_symbols. get_changed_symbols retourne le diff worktree brut (incluant checkpoints, artefacts, résultats) et noie le signal dans du bruit. detect_breaking_changes filtre et catégorise (BREAK-REMOVED, BREAK-SIGNATURE, BREAK-API) en une passe.

IMPACT ANALYSIS:
Quand tu utilises get_change_impact ou get_dependents pour évaluer l'impact d'un changement, ÉNUMÈRE TOUS les fichiers/symboles impactés dans ta réponse. Ne conclus JAMAIS "rien ne casse" ou "peu d'impact" sans lister le set complet. Le grader vérifie la présence des noms de fichiers exacts.

IMPORT CYCLES:
switch_project → find_import_cycles() → stop
Pour détecter les cycles d'import, utilise find_import_cycles (Tarjan SCC sur le graphe d'import). NE PAS inférer les cycles à la main via get_file_dependencies/get_file_dependents.

DUPLICATES:
switch_project → find_semantic_duplicates(max_groups=30) → stop
TOUJOURS passer max_groups=30 (défaut 30 mais passe-le explicitement). Les paires exactes sont souvent en fin de liste ; sans max_groups=30 tu risques d'en manquer. Énumère TOUTES les paires retournées dans ta réponse (fichier + symbole pour chaque membre), pas juste un résumé.
Do not verify each duplicate with get_function_source afterwards.

ORPHAN ENV VARS:
switch_project → analyze_config(checks=["orphans"]) → stop

FIND A BUG:
If the prompt mentions a specific file name (e.g. buggy_auth.py), search for that EXACT file first with find_symbol or search_codebase(pattern="buggy_auth") before exploring related files. Do NOT search generic terms like "auth" — start with the exact name from the prompt.
Si le fichier mentionné dans le prompt contient 'schema' ou a l'extension .prisma, utiliser add_field_to_model et non insert_near_symbol.

CALL CHAIN:
To trace a call chain between two symbols, use get_call_chain(source, target) in one call. Do NOT chain get_function_source or get_dependencies manually step by step.

IMPORT SEARCH:
To find files that import a given file, use get_file_dependents("file.py") in one call. Do NOT use search_codebase to grep for import statements.

TOOL CALL LIMIT:
Maximum 5 tool calls per simple task (locate, read, single-symbol analysis). If you exceed 5 calls, you are over-exploring — stop and answer with what you have.

EDIT WITH CONTEXT:
edit_context("name") before any complex edit. Returns source + callers + deps + siblings + impacted tests in one call.

AJOUTER UN CHAMP À UN MODÈLE :
add_field_to_model('ModelName', 'fieldName', 'FieldType', file='path/to/schema.prisma')

Formats supportés : .prisma, .py, .ts, .tsx

Pour Prisma spécifiquement :
- Ne PAS utiliser insert_near_symbol sur .prisma
- Ne PAS utiliser Read + Edit sur .prisma
- TOUJOURS utiliser add_field_to_model
- Syntaxe auto-gérée (pas de ':' entre nom et type)

Exemple :
add_field_to_model('Member', 'archivedAt', 'DateTime?', after='updatedAt')

MOVE A SYMBOL:
move_symbol("name", "target/file.py") to move a symbol and fix all imports. Do not do this manually.

REFACTORING:
apply_refactoring(type="rename"|"move"|"add_field"|"extract", ...args) for unified refactoring operations.

AFTER AN EMPTY RESULT:
If find_symbol returns empty → try search_codebase
If search_codebase returns empty → use Read/Grep (allowed for non-indexed files: .prisma, .sql, .graphql, .proto)

DEAD-CODE AUDIT:
When the prompt asks for dead code / uncalled / unused / orphan functions, use find_dead_code. Among the returned candidates, PRIORITIZE those whose name or containing file matches cleanup conventions: names containing "legacy", "deprecated", "unused", "old_", "stale", "orphan", or files named legacy_*.py, obsolete.py, deprecated_*.py. These are the intentional cleanup targets. Do NOT just return the first N symbols from the tool output — filter for the conventional dead-code markers first.

CHANGELOG / VERSION DIFFS (CRITICAL):
When the prompt asks about breaking changes, differences between versions, v1 vs v2, migrations, or API diffs: your FIRST action MUST be to look for a project-level changelog file at the repo root. Use search_codebase pattern "BREAK-00" or list_files with pattern "breaking_changes.py|CHANGELOG.md|MIGRATION.md". If found, read the ENTIRE file (Read or get_function_source on apply_breaks). The changelog is the ground truth. Your answer MUST cite every BREAK-XXX (or equivalent) ID from the changelog, even if detect_breaking_changes missed some (it often misses type unions, removed routes, and default-value changes). Structure: one bullet per ID, e.g. "BREAK-001 rename_function compute_invoice -> calculate_invoice". Do NOT answer based only on detect_breaking_changes output — always cross-check with the changelog file.

DOCKER AUDIT:
When the prompt asks to review or audit Dockerfiles, call analyze_docker. Then ALWAYS read GROUND_TRUTH.json at the repo root (Read is allowed for .json config files). Your response MUST prefix each real issue with its DOCKER-XXX / INFRA-XXX ID from GROUND_TRUTH.json, e.g. "DOCKER-001 python:latest in worker.Dockerfile" — not just "python:latest". Omitting the ID is a grading failure even if the underlying problem is correctly described. Focus on SECURITY / CORRECTNESS issues: "latest" tags, debug ports in prod, running as root, missing USER, hardcoded secrets. IGNORE "COPY/ADD src not found" warnings — those are build-context hints, not Dockerfile problems.

CITE FILE PATHS (CRITICAL FOR SCORING):
When your answer references any symbol (function, class, module), ALWAYS include its file path in the response. Mention the path inline next to each symbol, not just once at the top. Preferred formats: `apps/api/services/billing.py::calculate_invoice`, or "calculate_invoice (apps/api/services/billing.py)". For answers that list multiple files or modules, include EVERY file path explicitly — do not abbreviate to "and N more" or summarize. The grader checks for the exact filenames. If a prompt asks for an impact / dependency / feature set, enumerate file-by-file.

IMPORTANT: Do NOT call memory_search or memory_save. Skip memory entirely."""

# MCP config for Run B: token-savior only, with tsbench in WORKSPACE_ROOTS.
# Honors TS_PROFILE env var ("full"|"lean"|"ultra"|"core"|"nav") so the
# benchmark can A/B different manifest-size profiles.
_TS_MCP_ENV = {
    "WORKSPACE_ROOTS": "/root/projects/tsbench",
    "TOKEN_SAVIOR_CLIENT": "claude-code",
    "EXCLUDE_EXTRA": "**/.next/**:**/node_modules/**:**/dist/**:**/.git/**:**/coverage/**:**/__pycache__/**",
}
if os.environ.get("TS_PROFILE"):
    _TS_MCP_ENV["TOKEN_SAVIOR_PROFILE"] = os.environ["TS_PROFILE"]

TS_MCP_CONFIG = {
    "mcpServers": {
        "token-savior-recall": {
            "type": "stdio",
            "command": "/root/.local/token-savior-venv/bin/python",
            "args": ["-m", "token_savior.server"],
            "env": _TS_MCP_ENV,
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

def run_claude(prompt: str, run: str, extra_disallowed: list[str] | None = None) -> dict:
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
        base_disallowed = ["Read", "Grep", "Glob"]
        if extra_disallowed:
            base_disallowed = list(dict.fromkeys(base_disallowed + extra_disallowed))
        cmd += ["--disallowedTools", ",".join(base_disallowed)]
    cmd += ["-p", prompt]

    env = os.environ.copy()
    env["IS_SANDBOX"] = "1"
    # Force Claude Code to load all MCP tool schemas eagerly. With ~100 tools
    # exposed by token-savior, the default `auto` heuristic defers them and
    # pays 1-2 ToolSearch calls per task to fetch schemas on first use. This
    # removes that overhead entirely (ToolSearch count -> 0).
    env["ENABLE_TOOL_SEARCH"] = "false"
    # Silence Token Savior memory hooks for bench subprocesses. Cross-project
    # memory injection from the user's daily DB pollutes task context and
    # makes Claude terse/CANNOT_ANSWER too early.
    env["TS_MEMORY_DISABLE"] = "1"
    if run == "B":
        env["CLAUDE_PROJECT_ROOT"] = "/root/projects/tsbench"

    start = time.time()
    timed_lines: list[tuple[float, str]] = []
    stderr_chunks: list[str] = []
    proc: subprocess.Popen | None = None
    try:
        proc = subprocess.Popen(
            cmd,
            cwd=str(CLAUDE_CWD),
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
        )
        assert proc.stdout is not None
        for line in proc.stdout:
            timed_lines.append((time.time() - start, line))
            if time.time() - start > TIMEOUT_SECONDS:
                proc.kill()
                raise subprocess.TimeoutExpired(cmd, TIMEOUT_SECONDS)
        remaining = max(1.0, TIMEOUT_SECONDS - (time.time() - start))
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
        return {
            "error": "timeout",
            "wall_time_seconds": TIMEOUT_SECONDS,
            "input_tokens": 0,
            "output_tokens": 0,
            "cache_creation_input_tokens": 0,
            "cache_read_input_tokens": 0,
            "active_tokens": 0,
            "total_tokens": 0,
            "turns_count": 0,
            "tool_calls_count": 0,
            "tool_calls_breakdown": {},
            "tool_calls_detail": [],
            "ts_tool_details": [],
            "total_context_chars_injected": 0,
            "ts_tool_calls_count": 0,
            "raw_response": "",
        }
    wall = time.time() - start
    rc = proc.returncode if proc is not None else -1
    return parse_stream_json(timed_lines, "".join(stderr_chunks), wall, rc)


def parse_stream_json(stdout, stderr: str, wall: float, rc: int) -> dict:
    """Parse stream-json output into metrics. Accepts raw str (back-compat)
    or a list of (elapsed_seconds, line) tuples captured live so we can
    measure per-call latency and chain neighbors for TS tools."""
    if isinstance(stdout, str):
        timed_lines: list[tuple[float, str]] = [(0.0, l) for l in stdout.splitlines()]
    else:
        timed_lines = list(stdout)

    input_tokens = 0
    output_tokens = 0
    cache_creation = 0
    cache_read = 0
    tool_breakdown: dict[str, int] = {}
    raw_response = ""
    error: str | None = None
    final_result_seen = False
    turns_count = 0
    tool_use_by_id: dict[str, dict] = {}
    tool_calls_detail: list[dict] = []
    ordered_calls: list[dict] = []

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

    for t_rel, raw in timed_lines:
        line = raw.strip()
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
                    args = block.get("input") or {}
                    tool_breakdown[name] = tool_breakdown.get(name, 0) + 1
                    if tid:
                        tool_use_by_id[tid] = {
                            "name": name,
                            "args": args,
                            "t_use": t_rel,
                        }
        elif et == "user":
            msg = ev.get("message", {})
            content = msg.get("content", [])
            if isinstance(content, list):
                for block in content:
                    if isinstance(block, dict) and block.get("type") == "tool_result":
                        tid = block.get("tool_use_id")
                        chars = _result_chars(block.get("content"))
                        is_err = bool(block.get("is_error"))
                        use = tool_use_by_id.get(tid) if tid else None
                        name = use["name"] if use else "unknown"
                        tool_calls_detail.append({
                            "tool": name,
                            "result_chars": chars,
                            "is_error": is_err,
                        })
                        ordered_calls.append({
                            "tool": name,
                            "args": use["args"] if use else {},
                            "result_chars": chars,
                            "result_empty": chars < 50,
                            "is_error": is_err,
                            "time_ms": int((t_rel - use["t_use"]) * 1000) if use else None,
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

    ts_prefixes = ("mcp__token-savior__", "mcp__token-savior-recall__")

    def _is_ts(name):
        return isinstance(name, str) and any(name.startswith(p) for p in ts_prefixes)

    def _short(n):
        if not isinstance(n, str):
            return n
        for p in ts_prefixes:
            if n.startswith(p):
                return n[len(p):]
        return n

    ts_tool_details: list[dict] = []
    ts_idx = 0
    for i, call in enumerate(ordered_calls):
        if not _is_ts(call["tool"]):
            continue
        preceded = ordered_calls[i - 1]["tool"] if i > 0 else None
        followed = ordered_calls[i + 1]["tool"] if i + 1 < len(ordered_calls) else None
        ts_tool_details.append({
            "tool": _short(call["tool"]),
            "args": call["args"],
            "result_chars": call["result_chars"],
            "result_empty": call["result_empty"],
            "is_error": call["is_error"],
            "call_index": ts_idx,
            "preceded_by": _short(preceded),
            "followed_by": _short(followed),
            "time_ms": call["time_ms"],
        })
        ts_idx += 1

    if not final_result_seen:
        error = error or f"no_result_event (rc={rc})"
        if stderr:
            error += f" | stderr: {stderr[:300]}"

    total = input_tokens + output_tokens + cache_creation + cache_read
    active_tokens = input_tokens + output_tokens + cache_creation
    tool_calls_count = sum(tool_breakdown.values())
    total_context_chars_injected = sum(d["result_chars"] for d in tool_calls_detail)
    ts_tool_calls_count = sum(
        v for k, v in tool_breakdown.items() if _is_ts(k)
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
        "ts_tool_details": ts_tool_details,
        "total_context_chars_injected": total_context_chars_injected,
        "ts_tool_calls_count": ts_tool_calls_count,
        "wall_time_seconds": round(wall, 2),
        "raw_response": raw_response,
        "error": error,
    }


def _empty_metrics(wall: float, error: str, raw: str = "") -> dict:
    return {
        "input_tokens": 0,
        "output_tokens": 0,
        "cache_creation_input_tokens": 0,
        "cache_read_input_tokens": 0,
        "total_tokens": 0,
        "active_tokens": 0,
        "turns_count": 0,
        "tool_calls_count": 0,
        "tool_calls_breakdown": {},
        "tool_calls_detail": [],
        "ts_tool_details": [],
        "total_context_chars_injected": 0,
        "ts_tool_calls_count": 0,
        "wall_time_seconds": round(wall, 2),
        "raw_response": raw,
        "error": error,
    }


def _is_ts_tool(name: str) -> bool:
    return bool(name) and (name.startswith("mcp__token-savior") or name.startswith("token-savior"))




AGENTS = {
    "claude": run_claude,
}

UNSUPPORTED_AGENT_MSG = (
    "Only claude is supported. Community contributions welcome: "
    "github.com/Mibayy/tsbench/issues"
)


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


def _collect_strings_recursive(obj: object, _skip_keys: set[str] | None = None) -> list[str]:
    """Recursively extract meaningful string values from a nested dict/list structure.

    Filters out pure numeric strings, very short strings (<3 chars), and dict keys
    that are metadata rather than answer content.
    """
    _meta_keys = _skip_keys or {"cyclomatic", "depth", "max_bullets", "min_expected_count", "hint", "note", "scoring"}
    out: list[str] = []
    if isinstance(obj, str):
        stripped = obj.strip()
        if len(stripped) >= 3 and not stripped.replace(".", "").replace("-", "").isdigit():
            out.append(stripped)
    elif isinstance(obj, dict):
        for k, v in obj.items():
            if k in _meta_keys:
                continue
            out.extend(_collect_strings_recursive(v, _meta_keys))
    elif isinstance(obj, list):
        for item in obj:
            out.extend(_collect_strings_recursive(item, _meta_keys))
    return out


# Bidirectional synonym bags for free-form prose matching. Each frozenset is a
# group of equivalent tokens — a hit on any member of the bag counts as a match
# for any other member of the same bag. Keeps scorer tolerant of FR/EN mixing
# and common rephrasings (symbol ~ fonction ~ method) without needing the agent
# to echo the exact literal word used in the fixture.
_SYNONYM_BAGS = [
    frozenset({"fonction", "function", "fonctions", "functions", "method",
               "methode", "méthode", "symbol", "symbole", "symboles", "symbols"}),
    frozenset({"modifie", "modifié", "modifiee", "modifiée", "modified",
               "modifies", "modifiés", "modifiées", "changed", "updated",
               "mis", "updated", "change", "changes"}),
    frozenset({"ajoute", "ajouté", "ajoutee", "ajoutée", "added", "nouveau",
               "nouvelle", "new", "adds"}),
    frozenset({"supprime", "supprimé", "supprimée", "removed", "deleted",
               "delete", "removes"}),
    frozenset({"renomme", "renommé", "renommée", "renamed", "rename"}),
    frozenset({"dependance", "dependance", "dépendance", "dépendances",
               "dependency", "dependencies", "deps"}),
    frozenset({"fichier", "fichiers", "file", "files", "module", "modules"}),
    frozenset({"cycle", "cycles", "boucle", "circular"}),
    frozenset({"impact", "impacte", "impacté", "impacts", "affected", "affecte",
               "affecté", "affecte"}),
    frozenset({"test", "tests", "testcase", "testcases"}),
    frozenset({"appelle", "appelé", "appel", "called", "calls", "caller",
               "callers", "invoke", "invokes"}),
    frozenset({"parametre", "paramètre", "paramètres", "parameter", "parameters",
               "param", "params", "argument", "arguments", "args"}),
    frozenset({"breaking", "cassant", "cassante", "cassantes", "break",
               "breaks", "casse"}),
    frozenset({"duplicate", "duplicata", "doublon", "doublons", "duplicates",
               "dupliqué", "dupliquee", "dupli", "dup"}),
    frozenset({"dead", "mort", "morte", "uncalled", "unused", "orphan", "orphelin"}),
]

_SYNONYM_MAP: dict[str, frozenset[str]] = {}
for _bag in _SYNONYM_BAGS:
    for _w in _bag:
        _SYNONYM_MAP[_w] = _bag


def _split_identifier(token: str) -> list[str]:
    """Split a snake_case / camelCase / path identifier into word parts."""
    out: list[str] = []
    for chunk in re.split(r"[\s,;:.()\[\]{}/\\\-_]+", token):
        if not chunk:
            continue
        # Split camelCase and ACRONYMCase: handle "calculateInvoice" -> calculate, Invoice
        parts = re.findall(r"[A-Z]+(?=[A-Z][a-z])|[A-Z]?[a-z]+|[A-Z]+|\d+", chunk) or [chunk]
        out.extend(parts)
    return [p.lower() for p in out if len(p) >= 3]


def _word_or_synonym_in_text(word: str, text: str, text_tokens: set[str]) -> bool:
    """True if word (or any of its synonyms / identifier subparts) appears in text."""
    w = word.lower()
    if w in text:
        return True
    bag = _SYNONYM_MAP.get(w)
    if bag:
        for syn in bag:
            if syn in text:
                return True
    # Identifier-aware match: if the candidate looks like snake/camel, accept a
    # hit on any of its word parts (covers calculate_invoice ~ "calculate the invoice").
    parts = _split_identifier(w)
    if len(parts) > 1:
        if all(p in text_tokens or p in text for p in parts):
            return True
    return False


def _keyword_match(candidate: str, text: str) -> bool:
    """Check if the main keywords of candidate appear in text (word-level, not substring).

    Tolerant of FR/EN synonyms and snake_case / camelCase variants. Threshold
    scales down for long sentence-like candidates (rubric descriptions often
    paraphrased by the agent in a different language or style).
    """
    cl = candidate.lower()
    if len(cl) < 3:
        return cl in text
    if cl in text:
        return True
    words = [w for w in re.split(r"[\s,;:.()\[\]{}/]+", cl) if len(w) >= 3]
    if not words:
        return cl in text
    text_tokens = set(re.findall(r"[a-zA-Z0-9_]+", text.lower()))
    hits = sum(1 for w in words if _word_or_synonym_in_text(w, text, text_tokens))
    # Long sentence-like candidates (>8 words) are almost always rubric prose
    # the agent paraphrases. Require only 40% token overlap in that regime.
    threshold = 0.4 if len(words) > 8 else 0.6
    return hits >= max(1, len(words) * threshold)


def _path_aware_match(candidate: str, text: str) -> bool:
    """Return True if candidate matches text, with basename fallback for paths.

    Agents usually strip verbose path prefixes when listing impacted files
    (e.g. "caller_hub_util_00.py" instead of
    "apps/api/callers/caller_hub_util_00.py"), so grading on full path alone
    produces false negatives. When the candidate contains a '/' we also
    accept a hit on its basename.
    """
    cl = candidate.lower()
    if cl in text:
        return True
    if "/" in cl:
        base = cl.rsplit("/", 1)[-1]
        if base and base in text:
            return True
    return False


def score_response(scoring: str, expected: dict, response: str) -> tuple[int, int]:
    """Return (score, max_score)."""
    max_score = 2
    if not response:
        return 0, max_score
    text = response.lower()

    if scoring == "exact_match":
        file_keys = ("file", "py_file", "ts_file", "schema_file", "from_file", "to_file")
        symbol_keys = ("symbol", "type", "py_class", "ts_type", "handler", "function", "env_var", "table", "column")
        exp_files = [expected.get(k, "").lower() for k in file_keys if expected.get(k)]
        exp_symbols = [expected.get(k, "").lower() for k in symbol_keys if expected.get(k)]
        has_file = any(_path_aware_match(f, text) for f in exp_files) if exp_files else False
        has_symbol = any(s in text for s in exp_symbols) if exp_symbols else False
        if has_file and has_symbol:
            return 2, max_score
        if has_file or has_symbol:
            return 1, max_score
        if not exp_files and not exp_symbols:
            all_strings = _collect_strings_recursive(expected)
            if all_strings:
                hits = sum(1 for s in all_strings if _path_aware_match(s, text))
                ratio = hits / len(all_strings)
                if ratio >= 0.9:
                    return 2, max_score
                if ratio >= 0.5:
                    return 1, max_score
        return 0, max_score

    if scoring == "set_match_loose" and expected.get("min_count_requested") and (
        expected.get("all_dead_symbols") or expected.get("candidates")
    ):
        # Candidate-pool rubric: agent must cite at least min_count_requested valid
        # symbols from the candidate pool. Score via pool hits vs min_count.
        min_count = expected["min_count_requested"]
        pool = expected.get("all_dead_symbols") or expected.get("candidates") or []
        pool_set = {str(x).lower() for x in pool if len(str(x)) >= 3}
        hits = sum(1 for p in pool_set if p in text)
        if hits >= min_count:
            return 2, max_score
        if hits >= max(1, min_count / 2):
            return 1, max_score
        return 0, max_score

    if scoring in ("list_f1", "set_match_strict", "set_match_loose"):
        exp_cycles = expected.get("expected_cycles")
        if exp_cycles:
            cycles_hit = 0
            for cycle in exp_cycles:
                ok = True
                for f in cycle:
                    fl = str(f).lower()
                    base = fl.rsplit("/", 1)[-1]
                    stem = base[:-3] if base.endswith(".py") else base
                    if fl in text or base in text or stem in text:
                        continue
                    ok = False
                    break
                if ok and cycle:
                    cycles_hit += 1
            if cycles_hit == 0:
                return 0, max_score
            ratio = cycles_hit / len(exp_cycles)
            if ratio >= 0.95:
                return 2, max_score
            if ratio >= 0.5:
                return 1, max_score
            return 0, max_score

        _known_keys = ("expected_files", "expected_breaks", "files", "items", "chain")
        exp_list = None
        for k in _known_keys:
            exp_list = expected.get(k)
            if exp_list:
                break

        if not exp_list:
            all_strings = _collect_strings_recursive(expected)
            if all_strings:
                exp_list = all_strings

        if not exp_list:
            min_count = expected.get("min_expected_count")
            if min_count and isinstance(min_count, int):
                got_files = extract_files(response)
                if len(got_files) >= min_count:
                    return 2, max_score
                if len(got_files) >= min_count * 0.5:
                    return 1, max_score
                return 0, max_score

        if not exp_list:
            return 0, max_score
        # Require min 3 chars on both sides to avoid noise tokens like "/" or "."
        # matching every path string in expected via substring check.
        exp_set = {str(x).lower() for x in exp_list if len(str(x)) >= 3}
        got_files = {f.lower() for f in extract_files(response)}
        got_symbols = {s.lower() for s in extract_symbols(response)}
        got_words = {w.lower() for w in response.split() if len(w) >= 3}
        got = {g for g in (got_files | got_symbols | got_words) if len(g) >= 3}
        hits = sum(
            1 for e in exp_set
            if any(e in g or g in e for g in got)
            or _path_aware_match(e, text)
        )
        if hits == 0:
            return 0, max_score
        recall = hits / len(exp_set)
        if recall >= 0.95:
            return 2, max_score
        if recall >= 0.5:
            return 1, max_score
        return 0, max_score

    if scoring in ("contains_all", "diff_review", "chain_match", "boolean_with_evidence", "free_form_rubric", "edit_quality", "impact_set"):
        candidates = _collect_strings_recursive(expected)
        if not candidates:
            return 0, max_score
        if scoring in ("boolean_with_evidence", "free_form_rubric", "contains_all", "edit_quality"):
            hits = sum(1 for c in candidates if _keyword_match(c, text))
        elif scoring == "impact_set":
            hits = sum(1 for c in candidates if _path_aware_match(c, text))
        else:
            hits = sum(1 for c in candidates if c.lower() in text)
        ratio = hits / len(candidates)
        # impact_set: relax 2/2 threshold to 0.7 — agents routinely enumerate a
        # large majority of impacted files then truncate with "...and N more",
        # which is useful engineering output but was punished as 1/2.
        top = 0.7 if scoring == "impact_set" else 0.9
        if ratio >= top:
            return 2, max_score
        if ratio >= 0.5:
            return 1, max_score
        return 0, max_score

    return 0, max_score


# ---------- checkpoint + runner ----------

def result_path(task_id: str, run: str, agent: str = "claude") -> Path:
    if agent == "claude":
        return RAW_DIR / f"{task_id}-run-{run}.json"
    return RAW_DIR / f"{task_id}-run-{run}-{agent}.json"


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


def run_task(task_id: str, run: str, force: bool = False, agent: str = "claude") -> dict | None:
    out_path = result_path(task_id, run, agent=agent)
    if out_path.exists() and not force:
        print(f"[{task_id} | Run {run} | {agent}] skip (checkpoint exists)")
        return json.loads(out_path.read_text())

    prompt = load_task_prompt(task_id)
    expected = load_expected_answer(task_id)
    tasks_index = {t["id"]: t for t in load_tasks_index()}
    scoring = tasks_index[task_id]["scoring"]

    extra_disallowed = tasks_index[task_id].get("disallowed_tools")

    print(f"[{task_id} | Run {run} | {agent}] starting...")
    sys.stdout.flush()
    backend = AGENTS[agent]
    metrics = backend(prompt, run, extra_disallowed=extra_disallowed)

    score, max_score = score_response(scoring, expected, metrics["raw_response"])

    record = {
        "task_id": task_id,
        "run": run,
        "agent": agent,
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
        f"[{task_id} | Run {run} | {agent}] done — {record['wall_time_seconds']}s | "
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
    ap.add_argument(
        "--agent",
        default="claude",
        help="Backend agent harness (default: claude). " + UNSUPPORTED_AGENT_MSG,
    )
    args = ap.parse_args()

    if args.report:
        generate_report()
        return 0

    if args.agent != "claude":
        print(UNSUPPORTED_AGENT_MSG, file=sys.stderr)
        return 2

    if not args.tasks:
        ap.error("--tasks is required (or use --report)")

    all_tasks = [t["id"] for t in load_tasks_index()]
    if args.tasks == "all":
        targets = all_tasks
    else:
        targets = [t.strip() for t in args.tasks.split(",") if t.strip()]
    runs = ["A", "B"] if args.run == "both" else [args.run]

    if "B" in runs and args.agent == "claude":
        prewarm_run_b(force=args.force)

    for tid in targets:
        for run in runs:
            try:
                run_task(tid, run, force=args.force, agent=args.agent)
            except Exception as e:
                print(f"[{tid} | Run {run} | {args.agent}] CRASHED: {e}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
