import re
import unicodedata

__all__ = ["slugify"]


def slugify(text: str) -> str:
    """Convert a string to a URL-safe slug."""
    normalized = unicodedata.normalize('NFKD', text)
    ascii_text = normalized.encode('ascii', 'ignore').decode('ascii')
    ascii_text = ascii_text.lower()
    ascii_text = re.sub(r'[\s_]+', '-', ascii_text)
    ascii_text = re.sub(r'[^a-z0-9-]', '', ascii_text)
    ascii_text = re.sub(r'-+', '-', ascii_text)
    return ascii_text.strip('-')
