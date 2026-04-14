"""String helpers."""


def slugify(value: str) -> str:
    """Convert a string to a URL-safe slug."""
    return "-".join(value.lower().split())


def truncate(value: str, max_len: int = 100) -> str:
    """Truncate a string with ellipsis."""
    if len(value) <= max_len:
        return value
    return value[: max_len - 1] + "…"
