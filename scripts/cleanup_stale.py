#!/usr/bin/env python3
import argparse
import sys


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="cleanup_stale",
        description="Cleanup stale files (report or delete).",
    )
    parser.add_argument("--dry-run", action="store_true", help="Do not modify anything")
    parser.add_argument("--older-than", type=int, default=30, metavar="DAYS",
                        help="Age threshold in days (default: 30)")
    parser.add_argument("--path", type=str, required=True, nargs="+",
                        help="One or more paths to scan")

    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("report", help="Report stale files")
    subparsers.add_parser("delete", help="Delete stale files")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    print("Parsed arguments:")
    print(f"  command    = {args.command}")
    print(f"  dry_run    = {args.dry_run}")
    print(f"  older_than = {args.older_than} days")
    print(f"  paths      = {args.path}")
    sys.exit(0)


if __name__ == "__main__":
    main()
