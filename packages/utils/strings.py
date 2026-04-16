def slugify(value: str) -> str:
    """Convert a string to a URL-safe slug."""
    return "-".join(value.lower().split())