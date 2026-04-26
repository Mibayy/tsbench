#!/usr/bin/env python3
"""tsbench — synthetic benchmark project generator.

Reproducible with --seed. Produces a SaaS-shaped monorepo (~250 files, ~20k LOC)
with intentionally planted artifacts documented in GROUND_TRUTH.json.
"""
from __future__ import annotations
import argparse
import json
import os
import random
import shutil
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

ROOT = Path(__file__).parent.resolve()

# Directories we own and regenerate. Never touch generate.py, README.md, .git, etc.
MANAGED = [
    "apps", "packages", "infra", "config", "tests", "scripts", "docs",
    ".github",
]

# ============================================================
# Registry — tracks everything we create, for GROUND_TRUTH.json
# ============================================================
@dataclass
class Registry:
    artifacts: list[dict] = field(default_factory=list)
    files: list[str] = field(default_factory=list)
    loc_total: int = 0
    # For planters: index file -> list of (symbol_name, line, kind)
    symbols: dict[str, list[tuple[str, int, str]]] = field(default_factory=dict)
    # Callgraph we seed: caller fq_name -> set of callee fq_names
    callgraph: dict[str, set[str]] = field(default_factory=dict)

    def add_artifact(self, art: dict) -> None:
        self.artifacts.append(art)

    def add_symbol(self, file: str, name: str, line: int, kind: str) -> None:
        self.symbols.setdefault(file, []).append((name, line, kind))

    def record_call(self, caller_fq: str, callee_fq: str) -> None:
        self.callgraph.setdefault(caller_fq, set()).add(callee_fq)


REG = Registry()
RNG: random.Random = random.Random(42)


def rwrite(rel: str, content: str) -> None:
    """Write a file under ROOT and track it."""
    p = ROOT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content)
    REG.files.append(rel)
    REG.loc_total += content.count("\n") + (0 if content.endswith("\n") else 1)


def rwrite_py(rel: str, content: str) -> None:
    """Write a Python file and sanity-check it parses."""
    import ast
    try:
        ast.parse(content)
    except SyntaxError as e:
        print(f"[FATAL] generated Python is invalid at {rel}: {e}", file=sys.stderr)
        # Dump to /tmp for debugging
        (Path("/tmp") / "tsbench_bad.py").write_text(content)
        raise
    rwrite(rel, content)


# ============================================================
# Name pools (deterministic, drawn with RNG)
# ============================================================
DOMAINS = [
    "billing", "members", "sessions", "webhooks", "auth", "notifications",
    "reports", "audit", "exports", "integrations",
]
ENTITIES = [
    "Association", "Member", "Session", "Invoice", "Payment", "Webhook",
    "AuditLog", "Notification", "Report", "Export", "Subscription", "Plan",
    "Team", "Role", "Permission", "ApiKey", "Tenant", "Project", "Document",
    "Contract",
]
VERBS = [
    "create", "update", "delete", "fetch", "list", "find", "validate",
    "process", "dispatch", "compute", "resolve", "normalize", "serialize",
    "parse", "build", "apply", "schedule", "cancel", "commit", "rollback",
    "sync", "refresh", "archive", "restore",
]
ADJECTIVES = [
    "legacy", "pending", "active", "archived", "draft", "staged", "verified",
    "encrypted", "compressed", "cached", "primary", "secondary",
]


def pick(pool: list[str]) -> str:
    return RNG.choice(pool)


# ============================================================
# Python body templates — controlled LOC and cyclomatic complexity
# ============================================================
def py_body_simple(n_lines: int, var_prefix: str = "x") -> list[str]:
    lines = []
    for i in range(n_lines):
        op = i % 6
        if op == 0:
            lines.append(f"    {var_prefix}_{i} = {i} * 2 + 1")
        elif op == 1:
            lines.append(f"    {var_prefix}_{i} = '{pick(ADJECTIVES)}_{i}'")
        elif op == 2:
            lines.append(f"    {var_prefix}_{i} = [{i}, {i+1}, {i+2}, {i+3}]")
        elif op == 3:
            lines.append(f"    {var_prefix}_{i} = {{'k{i}': {i}, 'prev': {var_prefix}_{max(i-1, 0)}}}")
        elif op == 4:
            lines.append(f"    if {var_prefix}_{max(i-1, 0)} is not None:")
            lines.append(f"        {var_prefix}_{i} = str({var_prefix}_{max(i-1, 0)})")
            lines.append(f"    else:")
            lines.append(f"        {var_prefix}_{i} = ''")
        else:
            lines.append(f"    {var_prefix}_{i} = sum([j for j in range({i + 2}) if j % 2 == 0])")
    return lines


def py_body_complex(cyclomatic: int) -> list[str]:
    """Emit a function body with approximate cyclomatic complexity >= cyclomatic."""
    lines = ["    result = 0", "    items = list(range(10))"]
    branches_left = cyclomatic - 1
    i = 0
    while branches_left > 0:
        kind = i % 4
        if kind == 0:
            lines.append(f"    if result < {i * 3}:")
            lines.append(f"        result += {i} + 1")
            lines.append(f"    else:")
            lines.append(f"        result -= {i}")
            branches_left -= 2
        elif kind == 1:
            lines.append(f"    for it_{i} in items:")
            lines.append(f"        if it_{i} % 2 == 0:")
            lines.append(f"            result += it_{i}")
            lines.append(f"        elif it_{i} % 3 == 0:")
            lines.append(f"            result -= it_{i}")
            branches_left -= 3
        elif kind == 2:
            lines.append(f"    try:")
            lines.append(f"        result = result * {i + 1}")
            lines.append(f"    except ValueError:")
            lines.append(f"        result = -1")
            lines.append(f"    except KeyError:")
            lines.append(f"        result = -2")
            branches_left -= 2
        else:
            lines.append(f"    while result < {i * 10}:")
            lines.append(f"        if result == {i}:")
            lines.append(f"            break")
            lines.append(f"        result += 1")
            branches_left -= 2
        i += 1
    lines.append("    return result")
    return lines


def py_func(
    name: str,
    params: list[str] | None = None,
    body_lines: int = 8,
    complex_: int = 0,
    calls: list[str] | None = None,
    returns: str = "None",
    docstring: str | None = None,
) -> tuple[str, int]:
    """Generate a Python function. Returns (source, body_line_count)."""
    params = params or []
    params_str = ", ".join(params)
    lines = [f"def {name}({params_str}):"]
    doc = docstring or f"Handle {name.replace('_', ' ')}."
    lines.append(f'    """{doc}"""')
    if complex_ >= 2:
        lines.extend(py_body_complex(complex_))
    else:
        lines.extend(py_body_simple(body_lines))
        if calls:
            for c in calls:
                lines.append(f"    {c}")
        lines.append(f"    return {returns}")
    src = "\n".join(lines) + "\n"
    return src, len(lines)


def py_class(name: str, methods: list[tuple[str, list[str]]]) -> str:
    """Simple class with given methods (name, params)."""
    lines = [f"class {name}:"]
    lines.append(f'    """Domain model: {name}."""')
    lines.append(f"    def __init__(self, id: int, name: str = ''):")
    lines.append(f"        self.id = id")
    lines.append(f"        self.name = name")
    for mname, mparams in methods:
        params_str = ", ".join(["self"] + mparams)
        lines.append(f"    def {mname}({params_str}):")
        lines.append(f'        """Method {mname}."""')
        lines.append(f"        return self.id")
    return "\n".join(lines) + "\n"


# ============================================================
# TypeScript body templates
# ============================================================
def ts_func(
    name: str,
    params: list[str] | None = None,
    body_lines: int = 6,
    calls: list[str] | None = None,
    returns: str = "null",
    ret_type: str = "unknown",
    export: bool = True,
) -> str:
    params = params or []
    params_str = ", ".join(p if ":" in p else f"{p}: string" for p in params)
    prefix = "export " if export else ""
    lines = [f"{prefix}function {name}({params_str}): {ret_type} {{"]
    for i in range(body_lines):
        op = i % 5
        if op == 0:
            lines.append(f"  const v{i}: number = {i} * 2 + 1;")
        elif op == 1:
            lines.append(f"  const s{i}: string = `{pick(ADJECTIVES)}_${{{i}}}`;")
        elif op == 2:
            lines.append(f"  const arr{i}: number[] = [{i}, {i+1}, {i+2}, {i+3}];")
        elif op == 3:
            lines.append(f"  const obj{i} = {{ k: {i}, v: 'val_{i}', arr: [{i},{i+1}] }};")
        else:
            lines.append(f"  const mapped{i} = [{i},{i+1},{i+2}].map((x) => x * {i + 1});")
    if calls:
        for c in calls:
            lines.append(f"  {c};")
    lines.append(f"  return {returns};")
    lines.append("}")
    # Add some auxiliary exports per file for LOC and symbol count
    aux = []
    aux.append(f"export const {name}_VERSION = '0.1.0';")
    aux.append(f"export const {name}_MAX = 100;")
    aux.append(f"export type {name}Options = {{ mode: 'fast' | 'safe'; retries: number }};")
    aux.append(f"export interface {name}Result {{ ok: boolean; value?: unknown; error?: string }}")
    aux.append(f"export function {name}_default(): {name}Options {{")
    aux.append(f"  return {{ mode: 'safe', retries: 3 }};")
    aux.append(f"}}")
    return "\n".join(lines) + "\n\n" + "\n".join(aux) + "\n"


def ts_component(name: str, children_calls: list[str] | None = None) -> str:
    calls = children_calls or []
    lines = [
        f"import * as React from 'react';",
        "",
        f"export interface {name}Props {{",
        f"  id: string;",
        f"  label?: string;",
        f"  className?: string;",
        f"  variant?: 'default' | 'compact' | 'expanded';",
        f"  onAction?: (id: string) => void;",
        f"  disabled?: boolean;",
        f"}}",
        "",
        f"interface {name}State {{",
        f"  count: number;",
        f"  expanded: boolean;",
        f"  loading: boolean;",
        f"  error: string | null;",
        f"}}",
        "",
        f"const DEFAULT_STATE: {name}State = {{",
        f"  count: 0,",
        f"  expanded: false,",
        f"  loading: false,",
        f"  error: null,",
        f"}};",
        "",
        f"export function {name}(props: {name}Props) {{",
        f"  const [state, setState] = React.useState<{name}State>(DEFAULT_STATE);",
        f"  const {{ id, label, className, variant = 'default', onAction, disabled = false }} = props;",
        "",
        f"  const handleClick = React.useCallback(() => {{",
        f"    if (disabled) return;",
        f"    setState((s) => ({{ ...s, count: s.count + 1 }}));",
        f"    onAction?.(id);",
        f"  }}, [disabled, id, onAction]);",
        "",
        f"  const handleToggle = React.useCallback(() => {{",
        f"    setState((s) => ({{ ...s, expanded: !s.expanded }}));",
        f"  }}, []);",
        "",
        f"  React.useEffect(() => {{",
        f"    setState((s) => ({{ ...s, loading: true }}));",
        f"    const t = setTimeout(() => {{",
        f"      setState((s) => ({{ ...s, loading: false }}));",
        f"    }}, 10);",
        f"    return () => clearTimeout(t);",
        f"  }}, [id]);",
        "",
    ]
    for i, c in enumerate(calls):
        lines.append(f"  // link to {c}")
    lines.append(f"  if (state.error) {{")
    lines.append(f"    return <div className=\"error\">{{state.error}}</div>;")
    lines.append(f"  }}")
    lines.append("")
    lines.append(f"  return (")
    lines.append(f"    <div data-testid=\"{name.lower()}\" className={{`{name.lower()} ${{variant}} ${{className ?? ''}}`}}>")
    lines.append(f"      <header>")
    lines.append(f"        <span className=\"label\">{{label ?? id}}</span>")
    lines.append(f"        <button onClick={{handleToggle}} aria-label=\"toggle\">")
    lines.append(f"          {{state.expanded ? '▾' : '▸'}}")
    lines.append(f"        </button>")
    lines.append(f"      </header>")
    lines.append(f"      {{state.expanded && (")
    lines.append(f"        <section className=\"body\">")
    lines.append(f"          <p>Count: {{state.count}}</p>")
    lines.append(f"          <button onClick={{handleClick}} disabled={{disabled}}>")
    lines.append(f"            Increment")
    lines.append(f"          </button>")
    lines.append(f"        </section>")
    lines.append(f"      )}}")
    lines.append(f"      {{state.loading && <div className=\"spinner\">Loading…</div>}}")
    lines.append(f"    </div>")
    lines.append(f"  );")
    lines.append("}")
    return "\n".join(lines) + "\n"


# ============================================================
# Module generators
# ============================================================
API_SERVICES = [
    ("billing", "BillingService", ["compute_invoice", "apply_discount", "charge_customer", "refund_payment", "list_invoices", "void_invoice"]),
    ("members", "MemberService", ["create_member", "update_member", "deactivate_member", "list_members", "find_member_by_email", "bulk_import_members"]),
    ("sessions", "SessionService", ["create_session", "validate_session", "revoke_session", "extend_session", "list_user_sessions"]),
    ("webhooks", "WebhookService", ["dispatch_webhook", "retry_webhook", "verify_signature", "register_webhook", "list_webhooks"]),
    ("auth", "AuthService", ["authenticate_user", "issue_token", "revoke_token", "hash_password", "verify_password"]),
    ("notifications", "NotificationService", ["send_email", "send_sms", "render_template", "queue_notification", "list_notifications"]),
    ("reports", "ReportService", ["generate_monthly_report", "generate_ytd_report", "export_csv", "aggregate_metrics"]),
    ("audit", "AuditService", ["log_action", "query_logs", "purge_old_logs", "export_audit_trail"]),
    ("exports", "ExportService", ["start_export", "poll_export", "download_export", "cancel_export"]),
    ("integrations", "IntegrationService", ["connect_stripe", "sync_stripe_customers", "disconnect_stripe", "handle_stripe_event"]),
]


def gen_api_config() -> None:
    content = '''"""Application settings loaded from environment."""
import os
from dataclasses import dataclass


@dataclass
class Settings:
    database_url: str = os.environ.get("DATABASE_URL", "postgresql://localhost/tsbench")
    secret_key: str = os.environ.get("SECRET_KEY", "dev-secret")
    stripe_api_key: str = os.environ.get("STRIPE_API_KEY", "")
    stripe_webhook_secret: str = os.environ.get("STRIPE_WEBHOOK_SECRET", "")
    redis_url: str = os.environ.get("REDIS_URL", "redis://localhost:6379")
    log_level: str = os.environ.get("LOG_LEVEL", "INFO")
    allowed_origins: str = os.environ.get("ALLOWED_ORIGINS", "*")
    # UNDECL-001 / UNDECL-002 planted later
    max_page_size: int = int(os.environ.get("MAX_PAGE_SIZE", "100"))
    default_page_size: int = int(os.environ.get("DEFAULT_PAGE_SIZE", "20"))


settings = Settings()
'''
    rwrite_py("apps/api/config.py", content)


def gen_api_db() -> None:
    content = '''"""Database session factory (stub — not runnable)."""
from contextlib import contextmanager
from typing import Iterator


class DBSession:
    def __init__(self, url: str):
        self.url = url
        self.closed = False

    def query(self, model):
        return []

    def add(self, obj) -> None:
        pass

    def commit(self) -> None:
        pass

    def rollback(self) -> None:
        pass

    def close(self) -> None:
        self.closed = True


@contextmanager
def get_session(url: str = "postgresql://localhost/tsbench") -> Iterator[DBSession]:
    session = DBSession(url)
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def supabase_admin() -> DBSession:
    """Return a privileged DB session. CALLER-target for benchmark."""
    return DBSession("postgresql://localhost/tsbench?role=admin")
'''
    rwrite_py("apps/api/db.py", content)


def gen_api_models() -> None:
    for domain, cls_name, _ in API_SERVICES:
        methods = [
            ("save", []),
            ("delete", []),
            ("to_dict", []),
            ("validate", []),
            ("mark_dirty", []),
        ]
        body = f'"""Models for {domain}."""\n\n'
        body += py_class(cls_name.replace("Service", ""), methods)
        # add a child model
        body += "\n"
        body += py_class(f"{cls_name.replace('Service','')}Audit", [("record", ["action: str"])])
        rwrite_py(f"apps/api/models/{domain}.py", body)
    # __init__ re-exports
    lines = ['"""Models package."""']
    for domain, cls_name, _ in API_SERVICES:
        mn = cls_name.replace("Service", "")
        lines.append(f"from .{domain} import {mn}, {mn}Audit")
    rwrite_py("apps/api/models/__init__.py", "\n".join(lines) + "\n")


def gen_api_schemas() -> None:
    for domain, cls_name, _ in API_SERVICES:
        mn = cls_name.replace("Service", "")
        body = f'"""Pydantic-like schemas for {domain}."""\n\n'
        body += f"class {mn}Create:\n"
        body += f'    """Create payload for {mn}."""\n'
        body += f"    def __init__(self, name: str, owner_id: int):\n"
        body += f"        self.name = name\n"
        body += f"        self.owner_id = owner_id\n\n"
        body += f"class {mn}Update:\n"
        body += f'    """Update payload for {mn}."""\n'
        body += f"    def __init__(self, name: str = '', archived: bool = False):\n"
        body += f"        self.name = name\n"
        body += f"        self.archived = archived\n\n"
        body += f"class {mn}Response:\n"
        body += f'    """Read payload for {mn}."""\n'
        body += f"    def __init__(self, id: int, name: str):\n"
        body += f"        self.id = id\n"
        body += f"        self.name = name\n"
        rwrite_py(f"apps/api/schemas/{domain}.py", body)
    rwrite_py("apps/api/schemas/__init__.py", '"""Schemas package."""\n')


def gen_api_services() -> None:
    """Generate service files. Each service has multiple functions + callgraph."""
    extra_verbs = [
        "prepare", "finalize", "audit", "notify", "enqueue", "reconcile",
        "upsert", "expand", "reduce", "snapshot", "replay", "validate_input",
        "serialize_output", "deserialize_input", "build_context", "emit_metric",
        "rate_limit", "retry_with_backoff", "batch_process", "stream_process",
        "index_entity", "reindex_entity", "soft_delete", "hard_delete",
    ]
    for domain, cls_name, funcs in API_SERVICES:
        lines = [f'"""Service layer for {domain}."""']
        lines.append(f"from apps.api.db import get_session, supabase_admin")
        lines.append(f"from apps.api.models.{domain} import {cls_name.replace('Service','')}")
        lines.append(f"from apps.api.config import settings")
        lines.append(f"from apps.api.utils.logging import info, warn, error")
        lines.append(f"from apps.api.utils.errors import NotFoundError, ValidationError")
        lines.append("")
        helper = f"_{domain}_admin_db"
        lines.append(f"def {helper}():")
        lines.append(f'    """Internal admin DB accessor for {domain}."""')
        lines.append(f"    session = supabase_admin()")
        lines.append(f"    info('open admin session for {domain}')")
        lines.append(f"    return session")
        lines.append("")
        # main service functions (beefier)
        for fn in funcs:
            src, _ = py_func(
                fn,
                params=["payload: dict", "user_id: int = 0"],
                body_lines=18,
                calls=[
                    f"_ = {helper}()",
                    f"info('{fn} called by user {{}}'.format(user_id))",
                    f"_check = payload.get('check', True)",
                ],
                returns="{'ok': True, 'op': '" + fn + "', 'user': user_id}",
            )
            lines.append(src)
            REG.add_symbol(f"apps/api/services/{domain}.py", fn, 0, "function")
        # extra internal helpers per service for LOC weight
        for ev in extra_verbs:
            helper_name = f"{ev}_{domain}_internal"
            src, _ = py_func(
                helper_name,
                params=["data: dict"],
                body_lines=10,
                calls=[f"info('{helper_name} step')"],
                returns="data",
            )
            lines.append(src)
        rwrite_py(f"apps/api/services/{domain}.py", "\n".join(lines))


def gen_api_routers() -> None:
    for domain, cls_name, funcs in API_SERVICES:
        lines = [f'"""Routes for {domain}."""']
        lines.append(f"from apps.api.services import {domain} as svc")
        lines.append("")
        lines.append("ROUTES = []")
        lines.append("")

        def _register(method, path, handler):
            lines.append(f'ROUTES.append(("{method}", "{path}", "{handler}"))')

        _register("GET", f"/api/{domain}", f"list_{domain}")
        _register("POST", f"/api/{domain}", f"create_{domain}")
        _register("GET", f"/api/{domain}/{{id}}", f"get_{domain}")
        _register("PATCH", f"/api/{domain}/{{id}}", f"update_{domain}")
        _register("DELETE", f"/api/{domain}/{{id}}", f"delete_{domain}")
        _register("POST", f"/api/{domain}/{{id}}/members", f"add_member_to_{domain}")
        lines.append("")
        for h in [
            f"list_{domain}", f"create_{domain}", f"get_{domain}",
            f"update_{domain}", f"delete_{domain}", f"add_member_to_{domain}",
        ]:
            src, _ = py_func(
                h,
                params=["request: dict"],
                body_lines=14,
                calls=[
                    f"_ = svc.{funcs[0]}({{}}, 0)",
                    f"_body = request.get('body', {{}})",
                    f"_headers = request.get('headers', {{}})",
                ],
                returns="{'status': 'ok', 'handler': '" + h + "'}",
            )
            lines.append(src)
        rwrite_py(f"apps/api/routers/{domain}.py", "\n".join(lines))

    # main.py
    main = ['"""FastAPI app entrypoint (stub)."""']
    main.append("from apps.api.config import settings")
    for domain, _, _ in API_SERVICES:
        main.append(f"from apps.api.routers import {domain}")
    main.append("")
    main.append("class App:")
    main.append('    """Minimal app stub."""')
    main.append("    def __init__(self):")
    main.append("        self.routers = []")
    main.append("")
    main.append("def create_app():")
    main.append('    """Factory."""')
    main.append("    app = App()")
    for domain, _, _ in API_SERVICES:
        main.append(f"    app.routers.append({domain}.ROUTES)")
    main.append("    return app")
    main.append("")
    main.append("app = create_app()")
    rwrite_py("apps/api/main.py", "\n".join(main) + "\n")
    rwrite_py("apps/api/__init__.py", '"""tsbench api."""\n')
    rwrite_py("apps/api/routers/__init__.py", '"""Routers package."""\n')
    rwrite_py("apps/api/services/__init__.py", '"""Services package."""\n')


def gen_api_utils() -> None:
    util_files = {
        "apps/api/utils/pagination.py": '''"""Pagination helpers."""
from apps.api.config import settings


def paginate(items: list, page: int = 1, page_size: int = 0) -> dict:
    """Return a page slice of items.

    NOTE: page_size=0 falls back to settings.default_page_size.
    """
    if page_size <= 0:
        page_size = settings.default_page_size
    if page_size > settings.max_page_size:
        page_size = settings.max_page_size
    start = (page - 1) * page_size
    end = start + page_size
    return {"items": items[start:end], "page": page, "page_size": page_size, "total": len(items)}


def build_pagination_meta(total: int, page: int, page_size: int) -> dict:
    """Build pagination metadata."""
    return {"total": total, "page": page, "page_size": page_size, "pages": (total + page_size - 1) // page_size}
''',
        "apps/api/utils/strings.py": '''"""String helpers."""


def slugify(value: str) -> str:
    """Convert a string to a URL-safe slug."""
    return "-".join(value.lower().split())


def truncate(value: str, max_len: int = 100) -> str:
    """Truncate a string with ellipsis."""
    if len(value) <= max_len:
        return value
    return value[: max_len - 1] + "…"
''',
        "apps/api/utils/dates.py": '''"""Date helpers."""
from datetime import datetime, timedelta


def start_of_day(dt: datetime) -> datetime:
    """Return the start of the day for dt."""
    return dt.replace(hour=0, minute=0, second=0, microsecond=0)


def end_of_day(dt: datetime) -> datetime:
    """Return the end of the day for dt."""
    return dt.replace(hour=23, minute=59, second=59, microsecond=999999)


def days_between(a: datetime, b: datetime) -> int:
    """Number of whole days between two datetimes."""
    return abs((a - b).days)
''',
        "apps/api/utils/errors.py": '''"""Error classes."""


class TsbenchError(Exception):
    """Base error."""


class NotFoundError(TsbenchError):
    """Resource not found."""


class PermissionDenied(TsbenchError):
    """Caller does not have permission."""


class ValidationError(TsbenchError):
    """Invalid input."""
''',
        "apps/api/utils/logging.py": '''"""Lightweight logging wrapper."""
from apps.api.config import settings


def log(level: str, message: str) -> None:
    """Emit a log line (stub)."""
    if level.upper() == "DEBUG" and settings.log_level != "DEBUG":
        return
    print(f"[{level}] {message}")


def info(msg: str) -> None:
    log("INFO", msg)


def warn(msg: str) -> None:
    log("WARN", msg)


def error(msg: str) -> None:
    log("ERROR", msg)
''',
    }
    for path, content in util_files.items():
        rwrite_py(path, content)
    rwrite_py("apps/api/utils/__init__.py", '"""Utils package."""\n')


# ---------- worker ----------
def gen_worker() -> None:
    rwrite_py("apps/worker/__init__.py", '"""tsbench worker."""\n')
    main = '''"""Worker entrypoint."""
from apps.worker.dispatcher import Dispatcher


def main() -> int:
    """Start the worker loop."""
    d = Dispatcher()
    d.run_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
'''
    rwrite_py("apps/worker/main.py", main)
    dispatcher = '''"""Task dispatcher."""
from apps.worker.tasks import (
    billing_tasks, notification_tasks, export_tasks,
    webhook_tasks, session_tasks,
)


class Dispatcher:
    """Routes events to task handlers."""

    def __init__(self):
        self.handlers = {
            "billing": billing_tasks.handle,
            "notification": notification_tasks.handle,
            "export": export_tasks.handle,
            "webhook": webhook_tasks.handle,
            "session": session_tasks.handle,
        }

    def dispatch(self, kind: str, payload: dict) -> dict:
        """Send an event to its handler."""
        handler = self.handlers.get(kind)
        if handler is None:
            return {"status": "unknown_kind"}
        return handler(payload)

    def run_forever(self) -> None:
        """Event loop stub."""
        while False:
            pass
'''
    rwrite_py("apps/worker/dispatcher.py", dispatcher)
    # Task modules
    for kind in ["billing", "notification", "export", "webhook", "session"]:
        body = f'"""Task module: {kind}."""\n\n'
        body += f"def handle(payload: dict) -> dict:\n"
        body += f'    """Process a {kind} payload."""\n'
        body += f"    _ = process_step_one(payload)\n"
        body += f"    _ = process_step_two(payload)\n"
        body += f"    return {{'kind': '{kind}', 'ok': True}}\n\n"
        body += f"def process_step_one(payload: dict) -> int:\n"
        body += f'    """First step."""\n'
        body += f"    return len(payload)\n\n"
        body += f"def process_step_two(payload: dict) -> int:\n"
        body += f'    """Second step."""\n'
        body += f"    return sum(range(10))\n"
        rwrite_py(f"apps/worker/tasks/{kind}_tasks.py", body)
    rwrite_py("apps/worker/tasks/__init__.py", '"""Tasks."""\n')
    # Handlers (wrappers that call services via dispatcher — used later for chains)
    for i, kind in enumerate(["stripe", "postmark", "twilio", "slack"]):
        body = f'"""Handler: {kind}."""\n'
        body += f"from apps.worker.dispatcher import Dispatcher\n\n"
        body += f"_dispatcher = Dispatcher()\n\n"
        body += f"def handle_{kind}_event(event: dict) -> dict:\n"
        body += f'    """Incoming {kind} webhook handler."""\n'
        body += f"    return _dispatcher.dispatch('webhook', event)\n"
        rwrite_py(f"apps/worker/handlers/{kind}.py", body)
    rwrite_py("apps/worker/handlers/__init__.py", '"""Handlers."""\n')


# ---------- web (Next.js / TS) ----------
WEB_PAGES = [
    "dashboard", "members", "billing", "sessions", "webhooks", "notifications",
    "reports", "audit", "settings", "profile", "invite", "signup", "login",
    "forgot-password", "pricing",
]
WEB_COMPONENTS = [
    "MemberCard", "InvoiceList", "SessionBadge", "WebhookTable", "NotificationBell",
    "ReportChart", "AuditRow", "Sidebar", "TopBar", "PageHeader", "EmptyState",
    "ErrorBanner", "LoadingSpinner", "Modal", "ConfirmDialog", "Toast",
    "Pagination", "SearchInput", "FilterBar", "DataTable", "PricingCard",
    "Avatar", "Tooltip", "Dropdown", "Tabs",
]


def gen_web() -> None:
    # package.json
    pkg = {
        "name": "tsbench-web",
        "version": "0.1.0",
        "private": True,
        "scripts": {"build": "next build", "dev": "next dev", "lint": "eslint ."},
        "dependencies": {"next": "^15.0.0", "react": "^19.0.0", "react-dom": "^19.0.0"},
    }
    rwrite("apps/web/package.json", json.dumps(pkg, indent=2) + "\n")
    # tsconfig — relaxed: this is a benchmark target, not a runnable app
    tsconfig = {
        "compilerOptions": {
            "target": "ES2022",
            "lib": ["ES2022", "DOM"],
            "module": "ESNext",
            "moduleResolution": "Bundler",
            "jsx": "preserve",
            "strict": False,
            "noImplicitAny": False,
            "esModuleInterop": True,
            "skipLibCheck": True,
            "allowJs": True,
            "noEmit": True,
        },
        "include": ["**/*.ts", "**/*.tsx"],
    }
    rwrite("apps/web/tsconfig.json", json.dumps(tsconfig, indent=2) + "\n")

    # lib (api client, utils)
    for name in ["apiClient", "fetcher", "queryKeys", "errors", "format", "constants",
                 "permissions", "featureFlags", "analytics", "storage",
                 "dates", "urls", "validation", "errors2", "pricing"]:
        src = ts_func(name, ["input"], body_lines=4)
        rwrite(f"apps/web/lib/{name}.ts", src)

    # hooks
    for name in ["useMembers", "useBilling", "useSession", "useWebhooks",
                 "useNotifications", "useReports", "useAudit", "useSettings",
                 "useFeatureFlag", "useToasts"]:
        src = f'''import {{ useState, useEffect, useCallback, useMemo }} from 'react';

export interface {name}State<T> {{
  data: T | null;
  loading: boolean;
  error: Error | null;
  refetchCount: number;
}}

export interface {name}Options {{
  enabled?: boolean;
  refetchInterval?: number;
  staleTime?: number;
  onSuccess?: (data: unknown) => void;
  onError?: (error: Error) => void;
}}

const DEFAULT_OPTIONS: {name}Options = {{
  enabled: true,
  refetchInterval: 0,
  staleTime: 5000,
}};

export function {name}<T = unknown>(id: string, options: {name}Options = DEFAULT_OPTIONS) {{
  const [state, setState] = useState<{name}State<T>>({{
    data: null,
    loading: false,
    error: null,
    refetchCount: 0,
  }});

  const opts = useMemo(() => ({{ ...DEFAULT_OPTIONS, ...options }}), [options]);

  const fetchData = useCallback(async () => {{
    if (!opts.enabled) return;
    setState((s) => ({{ ...s, loading: true, error: null }}));
    try {{
      const result = {{ id }} as unknown as T;
      setState((s) => ({{
        ...s,
        data: result,
        loading: false,
        refetchCount: s.refetchCount + 1,
      }}));
      opts.onSuccess?.(result);
    }} catch (err) {{
      const error = err instanceof Error ? err : new Error(String(err));
      setState((s) => ({{ ...s, loading: false, error }}));
      opts.onError?.(error);
    }}
  }}, [id, opts]);

  useEffect(() => {{
    fetchData();
  }}, [fetchData]);

  useEffect(() => {{
    if (!opts.refetchInterval) return;
    const t = setInterval(fetchData, opts.refetchInterval);
    return () => clearInterval(t);
  }}, [fetchData, opts.refetchInterval]);

  const refetch = useCallback(() => fetchData(), [fetchData]);

  return {{ ...state, refetch }};
}}
'''
        rwrite(f"apps/web/hooks/{name}.ts", src)

    # types
    for name in ["member", "billing", "session", "webhook", "notification"]:
        cap = name.capitalize()
        src = f'''export interface {cap} {{
  id: string;
  name: string;
  email?: string;
  status: {cap}Status;
  role: {cap}Role;
  metadata: {cap}Metadata;
  createdAt: string;
  updatedAt: string;
  createdBy: string;
  archivedAt: string | null;
}}

export type {cap}Status = 'active' | 'pending' | 'archived' | 'draft';
export type {cap}Role = 'owner' | 'admin' | 'member' | 'viewer';

export interface {cap}Metadata {{
  tags: string[];
  customFields: Record<string, string | number | boolean>;
  source: 'web' | 'api' | 'import';
  version: number;
}}

export interface {cap}Summary {{
  id: string;
  label: string;
  status: {cap}Status;
}}

export interface {cap}CreateInput {{
  name: string;
  email?: string;
  role?: {cap}Role;
  metadata?: Partial<{cap}Metadata>;
}}

export interface {cap}UpdateInput {{
  name?: string;
  status?: {cap}Status;
  role?: {cap}Role;
  metadata?: Partial<{cap}Metadata>;
}}

export interface {cap}ListResponse {{
  items: {cap}[];
  total: number;
  page: number;
  pageSize: number;
}}

export const {cap}_DEFAULT_METADATA: {cap}Metadata = {{
  tags: [],
  customFields: {{}},
  source: 'web',
  version: 1,
}};
'''
        rwrite(f"apps/web/types/{name}.ts", src)

    # api client
    for name in ["members", "billing", "sessions", "webhooks", "notifications"]:
        cap = name.capitalize()
        src = f'''import {{ apiClient }} from '../lib/apiClient';
import {{ fetcher }} from '../lib/fetcher';

export interface {cap}Query {{
  page?: number;
  pageSize?: number;
  search?: string;
  status?: string;
  sortBy?: string;
  sortDir?: 'asc' | 'desc';
}}

const DEFAULT_QUERY: {cap}Query = {{
  page: 1,
  pageSize: 20,
  sortDir: 'asc',
}};

export async function list{cap}(params: {cap}Query = DEFAULT_QUERY) {{
  const query = {{ ...DEFAULT_QUERY, ...params }};
  const search = new URLSearchParams();
  if (query.page) search.set('page', String(query.page));
  if (query.pageSize) search.set('pageSize', String(query.pageSize));
  if (query.search) search.set('q', query.search);
  if (query.status) search.set('status', query.status);
  if (query.sortBy) search.set('sort', `${{query.sortBy}}:${{query.sortDir ?? 'asc'}}`);
  return apiClient(`/api/{name}?${{search.toString()}}`, {{}});
}}

export async function get{cap}(id: string) {{
  if (!id) throw new Error('id required');
  return apiClient(`/api/{name}/${{id}}`, {{}});
}}

export async function create{cap}(payload: Record<string, unknown>) {{
  const cleaned = Object.fromEntries(
    Object.entries(payload).filter(([, v]) => v !== undefined && v !== null),
  );
  return apiClient('/api/{name}', cleaned);
}}

export async function update{cap}(id: string, payload: Record<string, unknown>) {{
  return apiClient(`/api/{name}/${{id}}`, payload);
}}

export async function delete{cap}(id: string) {{
  return apiClient(`/api/{name}/${{id}}`, {{ _method: 'DELETE' }});
}}

export async function bulk{cap}(ids: string[], action: 'archive' | 'delete' | 'restore') {{
  return apiClient(`/api/{name}/bulk`, {{ ids, action }});
}}

export async function search{cap}(term: string) {{
  return fetcher(`/api/{name}/search?q=${{encodeURIComponent(term)}}`);
}}
'''
        rwrite(f"apps/web/api/{name}.ts", src)

    # components
    for comp in WEB_COMPONENTS:
        rwrite(f"apps/web/components/{comp}.tsx", ts_component(comp))

    # app pages
    for page in WEB_PAGES:
        cls = page.title().replace("-", "")
        body = f'''import * as React from 'react';
import {{ Sidebar }} from '../../components/Sidebar';
import {{ TopBar }} from '../../components/TopBar';
import {{ PageHeader }} from '../../components/PageHeader';
import {{ EmptyState }} from '../../components/EmptyState';
import {{ ErrorBanner }} from '../../components/ErrorBanner';
import {{ LoadingSpinner }} from '../../components/LoadingSpinner';
import {{ Pagination }} from '../../components/Pagination';

interface {cls}PageState {{
  page: number;
  pageSize: number;
  search: string;
  loading: boolean;
  error: string | null;
  items: unknown[];
}}

const INITIAL_STATE: {cls}PageState = {{
  page: 1,
  pageSize: 20,
  search: '',
  loading: false,
  error: null,
  items: [],
}};

export default function {cls}Page() {{
  const [state, setState] = React.useState<{cls}PageState>(INITIAL_STATE);

  const handleSearch = React.useCallback((term: string) => {{
    setState((s) => ({{ ...s, search: term, page: 1 }}));
  }}, []);

  const handlePageChange = React.useCallback((p: number) => {{
    setState((s) => ({{ ...s, page: p }}));
  }}, []);

  const handleRefresh = React.useCallback(() => {{
    setState((s) => ({{ ...s, loading: true, error: null }}));
  }}, []);

  React.useEffect(() => {{
    handleRefresh();
  }}, [handleRefresh, state.page, state.search]);

  if (state.error) {{
    return (
      <div>
        <Sidebar id="side" />
        <TopBar id="top" />
        <ErrorBanner id="err" label={{state.error}} />
      </div>
    );
  }}

  return (
    <div>
      <Sidebar id="side" />
      <TopBar id="top" />
      <PageHeader id="ph" label="{page}" />
      <main>
        {{state.loading && <LoadingSpinner id="sp" />}}
        {{!state.loading && state.items.length === 0 && (
          <EmptyState id="empty" label="No {page} yet" />
        )}}
        {{!state.loading && state.items.length > 0 && (
          <Pagination
            id="pag"
            label={{`Page ${{state.page}}`}}
          />
        )}}
      </main>
    </div>
  );
}}
'''
        rwrite(f"apps/web/app/{page}/page.tsx", body)
    rwrite("apps/web/app/layout.tsx", '''import * as React from 'react';

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return <html lang="en"><body>{children}</body></html>;
}
''')
    rwrite("apps/web/app/page.tsx", '''import * as React from 'react';

export default function HomePage() {
  return <h1>tsbench</h1>;
}
''')
    rwrite("apps/web/next.config.js", "module.exports = { reactStrictMode: true };\n")


# ---------- packages ----------
def gen_packages() -> None:
    # shared-types
    for name in ["common", "billing", "members", "sessions", "webhooks"]:
        src = f'''export interface {name.capitalize()}Id {{
  kind: '{name}';
  value: string;
}}

export type {name.capitalize()}Status = 'active' | 'pending' | 'archived';

export interface {name.capitalize()}Meta {{
  createdAt: string;
  updatedAt: string;
  createdBy: string;
}}
'''
        rwrite(f"packages/shared-types/{name}.ts", src)
    rwrite("packages/shared-types/package.json",
           json.dumps({"name": "@tsbench/shared-types", "version": "0.1.0"}, indent=2) + "\n")

    # db
    rwrite("packages/db/schema.prisma", '''generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

model Association {
  id        Int      @id @default(autoincrement())
  name      String
  ownerId   Int
  createdAt DateTime @default(now())
  archivedAt DateTime?
  members   Member[]
}

model Member {
  id            Int      @id @default(autoincrement())
  email         String   @unique
  role          String
  associationId Int
  association   Association @relation(fields: [associationId], references: [id])
  createdAt     DateTime @default(now())
}

model Invoice {
  id        Int     @id @default(autoincrement())
  amount    Int
  currency  String
  status    String
  memberId  Int
}
''')
    for i, name in enumerate(["0001_init", "0002_members", "0003_invoices", "0004_webhooks", "0005_audit"]):
        rwrite(f"packages/db/migrations/{name}.sql",
               f"-- Migration {name}\nCREATE TABLE IF NOT EXISTS {name.split('_',1)[1]} (id SERIAL PRIMARY KEY, name TEXT NOT NULL);\n")
    for name in ["seeds", "reset", "health", "helpers", "types",
                 "indexes", "constraints", "triggers", "views", "procedures"]:
        lines = [f'"""DB helper: {name}."""', ""]
        for verb in ["create", "apply", "rollback", "validate", "snapshot", "restore"]:
            fn_name = f"{name}_{verb}"
            src, _ = py_func(
                fn_name,
                params=["target: str"],
                body_lines=12,
                returns=f"'{{target}}'.format(target=target)",
            )
            lines.append(src)
        rwrite_py(f"packages/db/{name}.py", "\n".join(lines))
    rwrite_py("packages/db/__init__.py", '"""db package."""\n')

    # utils
    for name in ["crypto", "ids", "cache", "rate_limit", "retry",
                 "serialization", "compression", "circuit_breaker",
                 "metrics", "tracing", "sanitization", "escape"]:
        lines = [f'"""Util: {name}."""', ""]
        for verb in ["init", "apply", "reset", "configure", "validate",
                     "measure", "capture", "flush", "commit"]:
            fn_name = f"{name}_{verb}"
            src, _ = py_func(
                fn_name,
                params=["payload: dict", "options: dict | None = None"],
                body_lines=14,
                calls=[f"_opts = options or {{}}"],
                returns="{'util': '" + name + "', 'verb': '" + verb + "'}",
            )
            lines.append(src)
        rwrite_py(f"packages/utils/{name}.py", "\n".join(lines))
    rwrite_py("packages/utils/__init__.py", '"""utils."""\n')
    for name in ["format", "validate", "dates", "maps", "seq"]:
        src = ts_func(f"{name}All", ["input"], body_lines=3)
        rwrite(f"packages/utils/{name}.ts", src)


# ---------- infra ----------
def gen_infra() -> None:
    # Dockerfiles (3)
    # 1 — clean
    rwrite("infra/docker/api.Dockerfile", '''FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "-m", "apps.api.main"]
''')
    # 2 — uses :latest (DOCKER-001)
    rwrite("infra/docker/worker.Dockerfile", '''FROM python:latest
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "-m", "apps.worker.main"]
''')
    # 3 — exposes unnecessary port (DOCKER-002)
    rwrite("infra/docker/web.Dockerfile", '''FROM node:20-alpine
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci
COPY . .
RUN npm run build
EXPOSE 3000
EXPOSE 9229
EXPOSE 6666
CMD ["npm", "start"]
''')

    # k8s
    for kind in ["api", "worker", "web", "ingress"]:
        rwrite(f"infra/k8s/{kind}.yaml", f'''apiVersion: apps/v1
kind: Deployment
metadata:
  name: {kind}
spec:
  replicas: 1
  selector:
    matchLabels:
      app: {kind}
  template:
    metadata:
      labels:
        app: {kind}
    spec:
      containers:
        - name: {kind}
          image: tsbench/{kind}:latest
          ports:
            - containerPort: 8080
''')

    # terraform
    for name in ["main", "variables", "outputs"]:
        rwrite(f"infra/terraform/{name}.tf", f'# terraform {name}\n# placeholder\n')


# ---------- config ----------
def gen_config() -> None:
    # .env.example (declared env vars)
    env_example = '''# tsbench example env
DATABASE_URL=postgresql://localhost/tsbench
SECRET_KEY=change-me
STRIPE_API_KEY=
STRIPE_WEBHOOK_SECRET=
REDIS_URL=redis://localhost:6379
LOG_LEVEL=INFO
ALLOWED_ORIGINS=*
MAX_PAGE_SIZE=100
DEFAULT_PAGE_SIZE=20
# ORPHAN-001: declared but never read in code
LEGACY_SMTP_HOST=smtp.example.com
# ORPHAN-002
LEGACY_SMTP_PORT=587
# ORPHAN-003
UNUSED_FEATURE_FLAG=false
# ORPHAN-004
OLD_ANALYTICS_TOKEN=
'''
    rwrite("config/.env.example", env_example)

    # .env.staging with planted fake secrets (SECRET-001..003)
    # NOTE: values are intentionally non-matching placeholders so GitHub push
    # protection doesn't flag them. The benchmark detects these via VAR NAME
    # heuristics (STRIPE_API_KEY, AWS_SECRET_ACCESS_KEY, etc.), not value regex.
    env_staging = '''# tsbench STAGING env (synthetic, do not use)
DATABASE_URL=postgresql://staging:staging@db.example.com/tsbench
SECRET_KEY=tsbench_fake_secret_key_placeholder_001
# SECRET-001 — planted fake Stripe key (obfuscated placeholder)
STRIPE_API_KEY=tsbench_placeholder_stripe_key_do_not_scan
# SECRET-002 — planted fake webhook secret (obfuscated placeholder)
STRIPE_WEBHOOK_SECRET=tsbench_placeholder_webhook_secret_do_not_scan
# SECRET-003 — planted fake AWS key (obfuscated placeholder)
AWS_SECRET_ACCESS_KEY=tsbench_placeholder_aws_secret_do_not_scan
REDIS_URL=redis://redis.example.com:6379
LOG_LEVEL=INFO
ALLOWED_ORIGINS=https://tsbench.example.com
MAX_PAGE_SIZE=100
DEFAULT_PAGE_SIZE=20
LEGACY_SMTP_HOST=smtp.example.com
LEGACY_SMTP_PORT=587
UNUSED_FEATURE_FLAG=false
OLD_ANALYTICS_TOKEN=
'''
    rwrite("config/.env.staging", env_staging)

    # app.config.yaml
    rwrite("config/app.config.yaml", '''app:
  name: tsbench
  version: 0.1.0
features:
  billing: true
  exports: true
  audit: true
pagination:
  default: 20
  max: 100
timeouts:
  db: 5000
  http: 30000
''')


# ---------- tests ----------
def gen_tests() -> None:
    svc_domains = [d for d, _, _ in API_SERVICES]
    for kind in ["billing", "members", "sessions", "webhooks", "auth",
                 "notifications", "reports", "audit", "exports",
                 "pagination", "dates", "strings"]:
        lines = [f'"""Test {kind}."""']
        if kind in svc_domains:
            lines.append(f"from apps.api.services import {kind} as svc")
        lines.append("")
        for t in ["smoke", "empty_payload", "large_payload", "invalid_input",
                  "happy_path", "edge_case_none", "edge_case_zero",
                  "edge_case_unicode", "pagination_first_page",
                  "pagination_last_page"]:
            lines.append(f"def test_{kind}_{t}():")
            lines.append(f'    """Test {kind} — {t}."""')
            lines.append(f"    data = {{'kind': '{kind}', 'case': '{t}'}}")
            lines.append(f"    assert data['kind'] == '{kind}'")
            lines.append(f"    assert data['case'] == '{t}'")
            lines.append(f"    results = [i for i in range(5)]")
            lines.append(f"    assert len(results) == 5")
            lines.append("")
        rwrite_py(f"tests/test_{kind}.py", "\n".join(lines))
    # web tests (vitest)
    for comp in ["MemberCard", "InvoiceList", "Sidebar"]:
        rwrite(f"tests/web/{comp}.test.ts", f'''import {{ describe, it, expect }} from 'vitest';

describe('{comp}', () => {{
  it('renders', () => {{
    expect(true).toBe(true);
  }});
}});
''')


# ---------- scripts ----------
def gen_scripts() -> None:
    rwrite("scripts/setup.sh", '#!/usr/bin/env bash\nset -e\necho "setup"\n')
    rwrite("scripts/migrate.sh", '#!/usr/bin/env bash\nset -e\necho "migrate"\n')
    rwrite("scripts/deploy.sh", '#!/usr/bin/env bash\nset -e\necho "deploy"\n')
    rwrite_py("scripts/seed_data.py", '"""Seed data."""\n\ndef main() -> int:\n    """Seed."""\n    return 0\n\nif __name__ == "__main__":\n    raise SystemExit(main())\n')
    rwrite_py("scripts/backup.py", '"""Backup."""\n\ndef main() -> int:\n    """Backup."""\n    return 0\n\nif __name__ == "__main__":\n    raise SystemExit(main())\n')


# ---------- docs ----------
def gen_docs() -> None:
    for name in ["architecture", "getting-started", "api-reference", "deployment", "troubleshooting"]:
        rwrite(f"docs/{name}.md", f"# {name.replace('-',' ').title()}\n\nPlaceholder doc for tsbench.\n")


# ---------- workflows ----------
def gen_workflows() -> None:
    for wf in ["ci", "release", "nightly"]:
        rwrite(f".github/workflows/{wf}.yml", f'''name: {wf}
on: [push]
jobs:
  run:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: echo "{wf}"
''')


# ============================================================
# ARTIFACT PLANTERS
# ============================================================

def plant_dead_code() -> None:
    """DEAD-001..012 — exported functions never called anywhere."""
    # 12 functions distributed across api utils and packages
    plants = [
        ("apps/api/utils/legacy_helpers.py", "calculate_legacy_discount",
         "compute a deprecated discount rule"),
        ("apps/api/utils/legacy_helpers.py", "compute_legacy_tax",
         "compute legacy tax"),
        ("apps/api/utils/legacy_helpers.py", "format_legacy_invoice_id",
         "format old-style invoice id"),
        ("apps/api/utils/obsolete.py", "migrate_v1_session",
         "migrate a v1 session payload"),
        ("apps/api/utils/obsolete.py", "deprecated_webhook_signer",
         "sign a webhook using deprecated algorithm"),
        ("apps/api/utils/obsolete.py", "old_csv_exporter",
         "export to legacy CSV format"),
        ("packages/utils/orphaned.py", "unused_hash_helper",
         "hash helper, never called"),
        ("packages/utils/orphaned.py", "unused_validator",
         "validator, never called"),
        ("packages/utils/orphaned.py", "unused_formatter",
         "formatter, never called"),
        ("apps/worker/tasks/dead_tasks.py", "legacy_reaper",
         "reap expired legacy sessions"),
        ("apps/worker/tasks/dead_tasks.py", "orphan_cleaner",
         "clean orphan records"),
        ("apps/worker/tasks/dead_tasks.py", "stale_cache_purger",
         "purge stale cache entries"),
    ]
    # Group by file
    by_file: dict[str, list[tuple[str, str]]] = {}
    for path, fn, desc in plants:
        by_file.setdefault(path, []).append((fn, desc))
    for path, funcs in by_file.items():
        lines = [f'"""Legacy helpers (some dead) — {path}."""', ""]
        # Add one reachable function so the file isn't entirely dead (realism)
        lines.append("def still_used_helper(value: int) -> int:")
        lines.append('    """This one is called from main services."""')
        lines.append("    return value * 2")
        lines.append("")
        fn_lines: dict[str, int] = {}
        for fn, desc in funcs:
            fn_lines[fn] = len(lines) + 1
            lines.append(f"def {fn}(payload: dict) -> dict:")
            lines.append(f'    """{desc} — DEAD code."""')
            lines.append(f"    _noise = len(payload)")
            lines.append(f"    return {{'op': '{fn}', 'noise': _noise}}")
            lines.append("")
        rwrite_py(path, "\n".join(lines) + "\n")
        for fn, _ in funcs:
            dead_id = f"DEAD-{len([a for a in REG.artifacts if a['id'].startswith('DEAD-')]) + 1:03d}"
            REG.add_artifact({
                "id": dead_id,
                "category": "dead_code",
                "file": path,
                "symbol": fn,
                "line": fn_lines[fn],
                "description": f"Exported function never called: {fn}",
                "expected_answer": {"file": path, "symbol": fn},
            })


def plant_hotspots() -> None:
    """HOTSPOT-001..005 — functions with cyclomatic complexity >= 12."""
    specs = [
        ("apps/api/services/complex_billing.py", "reconcile_payments", 14),
        ("apps/api/services/complex_auth.py", "authenticate_multi_factor", 13),
        ("apps/worker/tasks/complex_pipeline.py", "orchestrate_nightly_job", 15),
        ("apps/api/utils/complex_validation.py", "validate_contract", 12),
        ("apps/api/services/complex_routing.py", "route_webhook_event", 14),
    ]
    for i, (path, name, cyclo) in enumerate(specs, start=1):
        src, n_lines = py_func(name, ["data: dict"], complex_=cyclo)
        full = f'"""Hotspot module — HOTSPOT-{i:03d}."""\n\n' + src
        rwrite_py(path, full)
        REG.add_artifact({
            "id": f"HOTSPOT-{i:03d}",
            "category": "hotspot",
            "file": path,
            "symbol": name,
            "line": 3,
            "cyclomatic_complexity": cyclo,
            "description": f"Function with cyclomatic complexity {cyclo}",
            "expected_answer": {"file": path, "symbol": name, "cyclomatic": cyclo},
        })


def plant_callers() -> None:
    """CALLER-001..004 — symbols with known caller counts 1, 3, 8, 20."""
    # Target function: pkg/utils helper. We create callers in dedicated files.
    target_specs = [
        ("lonely_util", 1),
        ("small_util", 3),
        ("medium_util", 8),
        ("hub_util", 20),
    ]
    target_file = "packages/utils/targeted.py"
    lines = ['"""CALLER-* targets — benchmark functions with known caller counts."""', ""]
    target_line_map: dict[str, int] = {}
    for tname, _ in target_specs:
        target_line_map[tname] = len(lines) + 1
        lines.append(f"def {tname}(payload: dict) -> dict:")
        lines.append(f'    """Target for CALLER benchmark."""')
        lines.append(f"    return dict(payload)")
        lines.append("")
    rwrite_py(target_file, "\n".join(lines) + "\n")

    # Now generate caller files
    caller_files_spec = []
    for idx, (tname, n_callers) in enumerate(target_specs, start=1):
        caller_paths = []
        for k in range(n_callers):
            cpath = f"apps/api/callers/caller_{tname}_{k:02d}.py"
            cbody = f'"""Caller {k} of {tname}."""\n'
            cbody += f"from packages.utils.targeted import {tname}\n\n"
            cbody += f"def do_it_{k}(payload: dict) -> dict:\n"
            cbody += f'    """Invoke {tname}."""\n'
            cbody += f"    return {tname}(payload)\n"
            rwrite_py(cpath, cbody)
            caller_paths.append(cpath)
        REG.add_artifact({
            "id": f"CALLER-{idx:03d}",
            "category": "callers",
            "target_symbol": tname,
            "target_file": target_file,
            "target_line": target_line_map[tname],
            "caller_count": n_callers,
            "caller_files": caller_paths,
            "description": f"Symbol {tname} has exactly {n_callers} caller(s)",
            "expected_answer": {
                "symbol": tname,
                "count": n_callers,
                "files": caller_paths,
            },
        })


def plant_chains() -> None:
    """CHAIN-001..003 — known A→B→C→D call chains."""
    specs = [
        ("apps/api/chains/alpha.py",
         ["alpha_entry", "alpha_middle", "alpha_inner", "alpha_leaf"]),
        ("apps/api/chains/beta.py",
         ["beta_entry", "beta_middle", "beta_inner", "beta_leaf"]),
        ("apps/api/chains/gamma.py",
         ["gamma_entry", "gamma_middle", "gamma_inner", "gamma_leaf"]),
    ]
    for i, (path, chain) in enumerate(specs, start=1):
        lines = [f'"""CHAIN-{i:03d} — call chain {" → ".join(chain)}."""', ""]
        # Emit in reverse so definitions come before callers
        for j, fn in enumerate(chain):
            if j == 0:  # leaf last
                pass
            lines.append(f"def {fn}(payload: dict) -> dict:")
            lines.append(f'    """Chain node: {fn}."""')
            if j < len(chain) - 1:
                next_fn = chain[j + 1]
                lines.append(f"    return {next_fn}(payload)")
            else:
                lines.append(f"    return {{'leaf': '{fn}'}}")
            lines.append("")
        # Python resolves at call-time, so forward-references work if called,
        # but to be ast.parse-safe, order doesn't matter. Leave as-is.
        rwrite_py(path, "\n".join(lines) + "\n")
        REG.add_artifact({
            "id": f"CHAIN-{i:03d}",
            "category": "call_chain",
            "file": path,
            "chain": chain,
            "description": f"Call chain: {' -> '.join(chain)}",
            "expected_answer": {"chain": chain, "file": path},
        })


def plant_cycles() -> None:
    """CYCLE-001..002 — intentional import cycles (Python)."""
    # Cycle 1: apps/api/cycles/mod_a <-> apps/api/cycles/mod_b
    rwrite_py("apps/api/cycles/mod_a.py", '''"""CYCLE-001 part A."""
from apps.api.cycles import mod_b


def a_call():
    """A calls B."""
    return mod_b.b_call()


def a_leaf():
    """Leaf of A."""
    return 1
''')
    rwrite_py("apps/api/cycles/mod_b.py", '''"""CYCLE-001 part B."""
from apps.api.cycles import mod_a


def b_call():
    """B calls A."""
    return mod_a.a_leaf()
''')
    rwrite_py("apps/api/cycles/__init__.py", '"""cycles package."""\n')
    REG.add_artifact({
        "id": "CYCLE-001",
        "category": "circular_dependency",
        "files": ["apps/api/cycles/mod_a.py", "apps/api/cycles/mod_b.py"],
        "description": "Import cycle between mod_a and mod_b",
        "expected_answer": {"cycle": ["apps/api/cycles/mod_a.py", "apps/api/cycles/mod_b.py"]},
    })

    # Cycle 2: 3-node cycle mod_x -> mod_y -> mod_z -> mod_x
    rwrite_py("apps/api/cycles/mod_x.py", '''"""CYCLE-002 part X."""
from apps.api.cycles import mod_y


def x_call():
    """X calls Y."""
    return mod_y.y_call()
''')
    rwrite_py("apps/api/cycles/mod_y.py", '''"""CYCLE-002 part Y."""
from apps.api.cycles import mod_z


def y_call():
    """Y calls Z."""
    return mod_z.z_call()
''')
    rwrite_py("apps/api/cycles/mod_z.py", '''"""CYCLE-002 part Z."""
from apps.api.cycles import mod_x


def z_call():
    """Z calls X."""
    return mod_x.x_call()
''')
    REG.add_artifact({
        "id": "CYCLE-002",
        "category": "circular_dependency",
        "files": [
            "apps/api/cycles/mod_x.py",
            "apps/api/cycles/mod_y.py",
            "apps/api/cycles/mod_z.py",
        ],
        "description": "3-node import cycle X → Y → Z → X",
        "expected_answer": {"cycle": [
            "apps/api/cycles/mod_x.py",
            "apps/api/cycles/mod_y.py",
            "apps/api/cycles/mod_z.py",
        ]},
    })


def plant_undeclared_envs() -> None:
    """UNDECL-001..002 — env vars read in code but not in .env.example."""
    rwrite_py("apps/api/utils/secret_reader.py", '''"""Reads some env vars."""
import os


def get_secret_config() -> dict:
    """Load secret config (reads SECRET_UNDECLARED_TOKEN)."""
    return {
        "token": os.environ.get("SECRET_UNDECLARED_TOKEN", ""),
        "region": os.environ.get("TSBENCH_HIDDEN_REGION", "us-east-1"),
    }
''')
    REG.add_artifact({
        "id": "UNDECL-001",
        "category": "undeclared_env",
        "file": "apps/api/utils/secret_reader.py",
        "env_var": "SECRET_UNDECLARED_TOKEN",
        "description": "Env var read in code but not in .env.example",
        "expected_answer": {"env_var": "SECRET_UNDECLARED_TOKEN"},
    })
    REG.add_artifact({
        "id": "UNDECL-002",
        "category": "undeclared_env",
        "file": "apps/api/utils/secret_reader.py",
        "env_var": "TSBENCH_HIDDEN_REGION",
        "description": "Env var read in code but not in .env.example",
        "expected_answer": {"env_var": "TSBENCH_HIDDEN_REGION"},
    })


def plant_orphans_and_secrets_metadata() -> None:
    """ORPHAN-001..004 and SECRET-001..003 — already placed in .env files; record IDs."""
    orphans = [
        ("LEGACY_SMTP_HOST", 1),
        ("LEGACY_SMTP_PORT", 2),
        ("UNUSED_FEATURE_FLAG", 3),
        ("OLD_ANALYTICS_TOKEN", 4),
    ]
    for var, idx in orphans:
        REG.add_artifact({
            "id": f"ORPHAN-{idx:03d}",
            "category": "orphan_env",
            "file": "config/.env.example",
            "env_var": var,
            "description": f"Env var declared in .env.example but never read in code",
            "expected_answer": {"env_var": var},
        })
    secrets = [
        ("STRIPE_API_KEY", "tsbench_placeholder_stripe", 1),
        ("STRIPE_WEBHOOK_SECRET", "tsbench_placeholder_webhook", 2),
        ("AWS_SECRET_ACCESS_KEY", "tsbench_placeholder_aws", 3),
    ]
    for var, val, idx in secrets:
        REG.add_artifact({
            "id": f"SECRET-{idx:03d}",
            "category": "leaked_secret",
            "file": "config/.env.staging",
            "env_var": var,
            "value_prefix": val[:12],
            "description": f"Fake secret planted in .env.staging: {var}",
            "expected_answer": {"env_var": var, "file": "config/.env.staging"},
        })


def plant_docker_issues() -> None:
    REG.add_artifact({
        "id": "DOCKER-001",
        "category": "docker_issue",
        "file": "infra/docker/worker.Dockerfile",
        "issue": "uses python:latest base image",
        "description": "Dockerfile uses :latest tag (non-reproducible)",
        "expected_answer": {"file": "infra/docker/worker.Dockerfile", "issue": "latest_tag"},
    })
    REG.add_artifact({
        "id": "DOCKER-002",
        "category": "docker_issue",
        "file": "infra/docker/web.Dockerfile",
        "issue": "exposes unnecessary ports 9229 and 6666",
        "description": "Dockerfile exposes debug/unused ports 9229 and 6666",
        "expected_answer": {"file": "infra/docker/web.Dockerfile", "ports": [9229, 6666]},
    })


def plant_dupes() -> None:
    """DUP-001..003 — semantically duplicate function pairs."""
    pairs = [
        (("apps/api/utils/pagination.py", "paginate"),
         ("packages/utils/paginate_copy.py", "paginate_also")),
        (("apps/api/utils/strings.py", "slugify"),
         ("packages/utils/slug_copy.py", "to_slug")),
        (("apps/api/utils/dates.py", "start_of_day"),
         ("packages/utils/date_copy.py", "day_start")),
    ]
    # Emit the copies
    rwrite_py("packages/utils/paginate_copy.py", '''"""DUP copy of paginate."""
from apps.api.config import DEFAULT_PAGE_SIZE


def paginate_also(items: list, page: int = 1, page_size: int = DEFAULT_PAGE_SIZE) -> dict:
    """Paginate a list (duplicate of apps/api/utils/pagination.paginate)."""
    if page_size <= 0:
        page_size = DEFAULT_PAGE_SIZE
    if page_size > 100:
        page_size = 100
    start = (page - 1) * page_size
    end = start + page_size
    return {"items": items[start:end], "page": page, "page_size": page_size, "total": len(items)}
''')
    rwrite_py("packages/utils/slug_copy.py", '''"""DUP copy of slugify."""


def to_slug(value: str) -> str:
    """Convert a string to a URL-safe slug (duplicate of slugify)."""
    return "-".join(value.lower().split())
''')
    rwrite_py("packages/utils/date_copy.py", '''"""DUP copy of start_of_day."""
from datetime import datetime


def day_start(dt: datetime) -> datetime:
    """Return the start of the day for dt (duplicate of start_of_day)."""
    return dt.replace(hour=0, minute=0, second=0, microsecond=0)
''')
    for i, (a, b) in enumerate(pairs, start=1):
        REG.add_artifact({
            "id": f"DUP-{i:03d}",
            "category": "semantic_duplicate",
            "pair": [{"file": a[0], "symbol": a[1]}, {"file": b[0], "symbol": b[1]}],
            "description": f"Semantic duplicate pair: {a[1]} ≡ {b[1]}",
            "expected_answer": {"pair": [a, b]},
        })


def plant_bugs() -> None:
    """BUG-001..002 — planted bugs."""
    rwrite_py("apps/api/utils/buggy_pagination.py", '''"""Buggy pagination — BUG-001 (off-by-one)."""


def buggy_paginate(items: list, page: int = 1, page_size: int = 10) -> list:
    """Return a page of items.

    BUG-001: the end index is wrong (`page_size + 1` instead of `page_size`),
    so each page returns 11 items instead of 10.
    """
    start = (page - 1) * page_size
    end = start + page_size + 1  # <-- off-by-one bug
    return items[start:end]
''')
    REG.add_artifact({
        "id": "BUG-001",
        "category": "planted_bug",
        "file": "apps/api/utils/buggy_pagination.py",
        "symbol": "buggy_paginate",
        "description": "Off-by-one in end index: returns 11 items instead of 10",
        "expected_answer": {"file": "apps/api/utils/buggy_pagination.py", "symbol": "buggy_paginate", "bug_line_hint": "end = start + page_size + 1"},
    })
    rwrite_py("apps/api/utils/buggy_auth.py", '''"""Buggy auth — BUG-002 (password comparison)."""


def buggy_verify_password(input_password: str, stored_hash: str) -> bool:
    """Verify password against hash.

    BUG-002: uses == for comparison (timing attack vulnerable) AND
    returns True if either is empty — logic error.
    """
    if not input_password or not stored_hash:
        return True  # <-- wrong, should be False
    return input_password == stored_hash
''')
    REG.add_artifact({
        "id": "BUG-002",
        "category": "planted_bug",
        "file": "apps/api/utils/buggy_auth.py",
        "symbol": "buggy_verify_password",
        "description": "Returns True when credentials are empty",
        "expected_answer": {"file": "apps/api/utils/buggy_auth.py", "symbol": "buggy_verify_password", "bug_line_hint": "return True"},
    })


def plant_ambiguous_symbols() -> None:
    """AMBIG-001..002 — same symbol name defined in two different modules."""
    # create_user in auth and in admin
    rwrite_py("apps/api/ambig/mod1.py", '''"""AMBIG-001 part 1."""


def create_user(email: str, role: str = "member") -> dict:
    """Create a regular user (AMBIG target 1/2)."""
    return {"email": email, "role": role, "module": "mod1"}


def process_event(event: dict) -> dict:
    """Process an event (AMBIG target 2/2)."""
    return {"event": event, "module": "mod1"}
''')
    rwrite_py("apps/api/ambig/mod2.py", '''"""AMBIG-001 part 2."""


def create_user(tenant_id: int, email: str) -> dict:
    """Create a tenant user (AMBIG target 1/2)."""
    return {"tenant_id": tenant_id, "email": email, "module": "mod2"}


def process_event(kind: str, payload: dict) -> dict:
    """Process an event (AMBIG target 2/2)."""
    return {"kind": kind, "payload": payload, "module": "mod2"}
''')
    rwrite_py("apps/api/ambig/__init__.py", '"""ambig package."""\n')
    REG.add_artifact({
        "id": "AMBIG-001",
        "category": "ambiguous_symbol",
        "symbol": "create_user",
        "locations": [
            {"file": "apps/api/ambig/mod1.py", "signature": "create_user(email: str, role: str)"},
            {"file": "apps/api/ambig/mod2.py", "signature": "create_user(tenant_id: int, email: str)"},
        ],
        "description": "Symbol 'create_user' defined in two modules with different signatures",
        "expected_answer": {"symbol": "create_user", "definitions": 2},
    })
    REG.add_artifact({
        "id": "AMBIG-002",
        "category": "ambiguous_symbol",
        "symbol": "process_event",
        "locations": [
            {"file": "apps/api/ambig/mod1.py", "signature": "process_event(event: dict)"},
            {"file": "apps/api/ambig/mod2.py", "signature": "process_event(kind: str, payload: dict)"},
        ],
        "description": "Symbol 'process_event' defined in two modules with different signatures",
        "expected_answer": {"symbol": "process_event", "definitions": 2},
    })


def record_breaking_changes_metadata() -> None:
    """BREAK-001..006 — documented in GROUND_TRUTH but only APPLIED by breaking_changes.py."""
    breaks = [
        {
            "id": "BREAK-001",
            "category": "breaking_change",
            "file": "apps/api/services/billing.py",
            "kind": "rename_function",
            "before": "compute_invoice",
            "after": "calculate_invoice",
            "description": "Rename compute_invoice -> calculate_invoice",
        },
        {
            "id": "BREAK-002",
            "category": "breaking_change",
            "file": "apps/api/services/auth.py",
            "kind": "signature_change",
            "symbol": "authenticate_user",
            "before": "authenticate_user(payload: dict, user_id: int = 0)",
            "after": "authenticate_user(credentials: dict)",
            "description": "Drop user_id param, rename payload->credentials",
        },
        {
            "id": "BREAK-003",
            "category": "breaking_change",
            "file": "apps/api/services/members.py",
            "kind": "remove_function",
            "symbol": "bulk_import_members",
            "description": "Remove bulk_import_members — consumers must migrate",
        },
        {
            "id": "BREAK-004",
            "category": "breaking_change",
            "file": "packages/shared-types/members.ts",
            "kind": "type_change",
            "before": "MembersStatus = 'active' | 'pending' | 'archived'",
            "after": "MembersStatus = 'active' | 'archived'",
            "description": "Remove 'pending' from MembersStatus union",
        },
        {
            "id": "BREAK-005",
            "category": "breaking_change",
            "file": "apps/api/routers/webhooks.py",
            "kind": "route_removed",
            "before": "DELETE /api/webhooks/{id}",
            "description": "Remove DELETE route",
        },
        {
            "id": "BREAK-006",
            "category": "breaking_change",
            "file": "apps/api/utils/pagination.py",
            "kind": "default_change",
            "before": "page_size default 20",
            "after": "page_size default 50",
            "description": "Change default page size from 20 to 50",
        },
    ]
    for b in breaks:
        REG.add_artifact(b)


# ============================================================
# MAIN
# ============================================================
def clean() -> None:
    for d in MANAGED:
        p = ROOT / d
        if p.exists():
            shutil.rmtree(p)
    gt = ROOT / "GROUND_TRUTH.json"
    if gt.exists():
        gt.unlink()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--clean", action="store_true",
                    help="Remove managed dirs before generating")
    args = ap.parse_args()

    global RNG
    RNG = random.Random(args.seed)

    if args.clean:
        clean()

    # Core project
    gen_api_config()
    gen_api_db()
    gen_api_models()
    gen_api_schemas()
    gen_api_services()
    gen_api_routers()
    gen_api_utils()
    gen_worker()
    gen_web()
    gen_packages()
    gen_infra()
    gen_config()
    gen_tests()
    gen_scripts()
    gen_docs()
    gen_workflows()

    # Artifact planters
    plant_dead_code()
    plant_hotspots()
    plant_callers()
    plant_chains()
    plant_cycles()
    plant_undeclared_envs()
    plant_orphans_and_secrets_metadata()
    plant_docker_issues()
    plant_dupes()
    plant_bugs()
    plant_ambiguous_symbols()
    record_breaking_changes_metadata()

    # Emit ground truth
    gt = {
        "seed": args.seed,
        "generator_version": "0.1.0",
        "summary": {
            "files_generated": len(REG.files),
            "loc_total": REG.loc_total,
            "artifacts_count": len(REG.artifacts),
        },
        "artifacts": REG.artifacts,
    }
    # Sort artifacts by id for determinism
    gt["artifacts"].sort(key=lambda a: a["id"])
    (ROOT / "GROUND_TRUTH.json").write_text(json.dumps(gt, indent=2) + "\n")

    # Per-category summary
    by_cat: dict[str, int] = {}
    for a in REG.artifacts:
        by_cat[a["category"]] = by_cat.get(a["category"], 0) + 1

    print(f"\n=== tsbench generated (seed={args.seed}) ===")
    print(f"Files:     {len(REG.files)}")
    print(f"LOC:       {REG.loc_total}")
    print(f"Artifacts: {len(REG.artifacts)}")
    print("By category:")
    for cat, n in sorted(by_cat.items()):
        print(f"  {cat:25s} {n}")
    print(f"\nGROUND_TRUTH.json written to {ROOT}/GROUND_TRUTH.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
