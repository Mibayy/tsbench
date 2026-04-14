"""Pagination helpers."""
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
