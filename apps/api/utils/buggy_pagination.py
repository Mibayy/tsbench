"""Buggy pagination — BUG-001 (off-by-one)."""


def buggy_paginate(items: list, page: int = 1, page_size: int = 10) -> list:
    """Return a page of items."""
    start = (page - 1) * page_size
    end = start + page_size
    return items[start:end]
