"""Pagination utility."""


import math


def paginate(items: list, page: int, per_page: int) -> dict:
    if per_page <= 0:
        raise ValueError("per_page must be > 0")
    if page <= 0:
        raise ValueError("page must be >= 1")

    total = len(items)
    total_pages = (total + per_page - 1) // per_page if total > 0 else 0

    if total_pages > 0 and page > total_pages:
        raise ValueError(f"page {page} exceeds total_pages {total_pages}")

    start = (page - 1) * per_page
    end = start + per_page
    page_items = items[start:end]

    return {
        "items": page_items,
        "page": page,
        "per_page": per_page,
        "total": total,
        "total_pages": total_pages,
        "has_next": page < total_pages,
        "has_prev": page > 1,
    }
