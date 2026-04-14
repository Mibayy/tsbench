"""DUP copy of paginate."""


def paginate_also(items: list, page: int = 1, page_size: int = 20) -> dict:
    """Paginate a list (duplicate of apps/api/utils/pagination.paginate)."""
    if page_size <= 0:
        page_size = 20
    if page_size > 100:
        page_size = 100
    start = (page - 1) * page_size
    end = start + page_size
    return {"items": items[start:end], "page": page, "page_size": page_size, "total": len(items)}
