"""Lightweight logging wrapper."""
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
