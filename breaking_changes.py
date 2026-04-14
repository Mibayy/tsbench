#!/usr/bin/env python3
"""Apply the 6 breaking changes (BREAK-001..006) to tsbench v1 → v2.

Run once, after v1 is tagged. Updates files in place and rewrites the
BREAK-* entries in GROUND_TRUTH.json with concrete before/after diffs.

Idempotent: safe to run multiple times (re-applies string replacements
and updates metadata; files end in the v2 state regardless).
"""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent.resolve()


def edit(rel: str, old: str, new: str, required: bool = True) -> bool:
    p = ROOT / rel
    if not p.exists():
        if required:
            raise FileNotFoundError(f"Missing file for edit: {rel}")
        return False
    content = p.read_text()
    if old not in content:
        if new in content:
            # Already applied
            return True
        if required:
            raise ValueError(f"Expected string not found in {rel}:\n{old!r}")
        return False
    p.write_text(content.replace(old, new))
    return True


def delete_block_py(rel: str, func_name: str) -> bool:
    """Delete a Python function block by name from a generated file.

    Relies on the fact that every generated function ends with a blank line
    before the next `def ` (py_func emits "\\n" at end, then rwrite joins with "\\n").
    """
    p = ROOT / rel
    content = p.read_text()
    pattern = re.compile(
        rf"(?ms)^def {re.escape(func_name)}\(.*?^(?=def |\Z)"
    )
    new_content, n = pattern.subn("", content)
    if n == 0:
        if f"def {func_name}(" in content:
            raise ValueError(f"Could not match block for {func_name} in {rel}")
        return False
    p.write_text(new_content)
    return True


def delete_line(rel: str, substring: str) -> bool:
    p = ROOT / rel
    content = p.read_text()
    new_lines = [ln for ln in content.splitlines() if substring not in ln]
    new_content = "\n".join(new_lines) + ("\n" if content.endswith("\n") else "")
    if new_content != content:
        p.write_text(new_content)
        return True
    return False


def apply_breaks() -> list[dict]:
    applied: list[dict] = []

    # BREAK-001: rename compute_invoice -> calculate_invoice in services/billing.py + router
    edit("apps/api/services/billing.py",
         "def compute_invoice(",
         "def calculate_invoice(")
    edit("apps/api/services/billing.py",
         "'op': 'compute_invoice'",
         "'op': 'calculate_invoice'")
    edit("apps/api/routers/billing.py",
         "svc.compute_invoice",
         "svc.calculate_invoice")
    applied.append({
        "id": "BREAK-001",
        "category": "breaking_change",
        "kind": "rename_function",
        "file": "apps/api/services/billing.py",
        "before": "compute_invoice",
        "after": "calculate_invoice",
        "description": "Rename compute_invoice -> calculate_invoice",
        "expected_answer": {
            "symbol_renamed": "compute_invoice -> calculate_invoice",
            "files_touched": ["apps/api/services/billing.py", "apps/api/routers/billing.py"],
        },
    })

    # BREAK-002: signature change for authenticate_user in services/auth.py
    # From: def authenticate_user(payload: dict, user_id: int = 0):
    # To:   def authenticate_user(credentials: dict):
    edit("apps/api/services/auth.py",
         "def authenticate_user(payload: dict, user_id: int = 0):",
         "def authenticate_user(credentials: dict):")
    # Router still calls with 2 args — that's intentional (breaking)
    applied.append({
        "id": "BREAK-002",
        "category": "breaking_change",
        "kind": "signature_change",
        "file": "apps/api/services/auth.py",
        "symbol": "authenticate_user",
        "before": "authenticate_user(payload: dict, user_id: int = 0)",
        "after": "authenticate_user(credentials: dict)",
        "description": "Drop user_id param, rename payload->credentials",
        "expected_answer": {
            "symbol": "authenticate_user",
            "file": "apps/api/services/auth.py",
            "kind": "signature_change",
        },
    })

    # BREAK-003: remove bulk_import_members from services/members.py
    delete_block_py("apps/api/services/members.py", "bulk_import_members")
    applied.append({
        "id": "BREAK-003",
        "category": "breaking_change",
        "kind": "remove_function",
        "file": "apps/api/services/members.py",
        "symbol": "bulk_import_members",
        "description": "Remove bulk_import_members from members service",
        "expected_answer": {
            "symbol": "bulk_import_members",
            "file": "apps/api/services/members.py",
            "kind": "removed",
        },
    })

    # BREAK-004: remove 'pending' from MembersStatus type
    edit("packages/shared-types/members.ts",
         "export type MembersStatus = 'active' | 'pending' | 'archived';",
         "export type MembersStatus = 'active' | 'archived';")
    applied.append({
        "id": "BREAK-004",
        "category": "breaking_change",
        "kind": "type_change",
        "file": "packages/shared-types/members.ts",
        "before": "MembersStatus = 'active' | 'pending' | 'archived'",
        "after": "MembersStatus = 'active' | 'archived'",
        "description": "Remove 'pending' from MembersStatus union",
        "expected_answer": {
            "type": "MembersStatus",
            "file": "packages/shared-types/members.ts",
            "removed_member": "pending",
        },
    })

    # BREAK-005: remove DELETE /api/webhooks/{id} route
    delete_line("apps/api/routers/webhooks.py",
                '("DELETE", "/api/webhooks/{id}"')
    # Also remove its handler block to keep the file clean
    delete_block_py("apps/api/routers/webhooks.py", "delete_webhooks")
    applied.append({
        "id": "BREAK-005",
        "category": "breaking_change",
        "kind": "route_removed",
        "file": "apps/api/routers/webhooks.py",
        "before": "DELETE /api/webhooks/{id}",
        "description": "Remove DELETE /api/webhooks/{id} route + handler",
        "expected_answer": {
            "route": "DELETE /api/webhooks/{id}",
            "file": "apps/api/routers/webhooks.py",
        },
    })

    # BREAK-006: change DEFAULT_PAGE_SIZE default 20 -> 50 in apps/api/config.py
    edit("apps/api/config.py",
         'default_page_size: int = int(os.environ.get("DEFAULT_PAGE_SIZE", "20"))',
         'default_page_size: int = int(os.environ.get("DEFAULT_PAGE_SIZE", "50"))')
    applied.append({
        "id": "BREAK-006",
        "category": "breaking_change",
        "kind": "default_change",
        "file": "apps/api/config.py",
        "before": 'DEFAULT_PAGE_SIZE default "20"',
        "after": 'DEFAULT_PAGE_SIZE default "50"',
        "description": "Change DEFAULT_PAGE_SIZE default from 20 to 50",
        "expected_answer": {
            "env_var": "DEFAULT_PAGE_SIZE",
            "file": "apps/api/config.py",
            "before": "20",
            "after": "50",
        },
    })

    return applied


def update_ground_truth(breaks: list[dict]) -> None:
    gt_path = ROOT / "GROUND_TRUTH.json"
    gt = json.loads(gt_path.read_text())
    # Remove stub BREAK-* entries and re-insert the concrete ones
    gt["artifacts"] = [a for a in gt["artifacts"] if not a["id"].startswith("BREAK-")]
    gt["artifacts"].extend(breaks)
    gt["artifacts"].sort(key=lambda a: a["id"])
    gt["version"] = "v2"
    gt_path.write_text(json.dumps(gt, indent=2) + "\n")


def main() -> int:
    print("Applying breaking changes v1 -> v2...")
    applied = apply_breaks()
    update_ground_truth(applied)

    # Validate all Python files still parse
    import ast
    errors = []
    for p in ROOT.rglob("*.py"):
        if ".git" in p.parts:
            continue
        try:
            ast.parse(p.read_text())
        except SyntaxError as e:
            errors.append(f"{p.relative_to(ROOT)}: {e}")
    if errors:
        print("SYNTAX ERRORS after applying breaks:", file=sys.stderr)
        for e in errors:
            print(f"  {e}", file=sys.stderr)
        return 1

    print(f"\nApplied {len(applied)} breaking changes:")
    for b in applied:
        print(f"  {b['id']}: {b['description']}")
    print("\nGROUND_TRUTH.json updated to v2.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
