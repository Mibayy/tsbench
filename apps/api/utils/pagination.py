"""Pagination helpers."""
from apps.api.config import DEFAULT_PAGE_SIZE, settings


def paginate(items: list, page: int = 1, per_page: int = DEFAULT_PAGE_SIZE) -> dict:
    """Paginate a list of items. page is 1-indexed."""
    if per_page <= 0:
        raise ValueError("per_page must be greater than 0")
    if page <= 0:
        raise ValueError("page must be greater than 0")
    
    total = len(items)
    total_pages = (total + per_page - 1) // per_page  # Ceiling division
    
    if page > total_pages and total > 0:
        raise ValueError(f"page {page} exceeds total_pages {total_pages}")
    
    start = (page - 1) * per_page
    end = start + per_page
    
    return {
        "items": items[start:end],
        "page": page,
        "per_page": per_page,
        "total": total,
        "total_pages": total_pages,
        "has_next": page < total_pages,
        "has_prev": page > 1,
    }


def build_pagination_meta(total: int, page: int, page_size: int = DEFAULT_PAGE_SIZE) -> dict:
    """Build pagination metadata."""
    return {"total": total, "page": page, "page_size": page_size, "pages": (total + page_size - 1) // page_size}
