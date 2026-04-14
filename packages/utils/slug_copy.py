"""DUP copy of slugify."""


def to_slug(value: str) -> str:
    """Convert a string to a URL-safe slug (duplicate of slugify)."""
    return "-".join(value.lower().split())
