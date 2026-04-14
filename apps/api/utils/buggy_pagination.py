"""Buggy pagination — BUG-001 (off-by-one)."""


def buggy_paginate(items: list, page: int = 1, page_size: int = 10) -> list:
    """Return a page of items.

    BUG-001: the end index is wrong (`page_size + 1` instead of `page_size`),
    so each page returns 11 items instead of 10.
    """
    start = (page - 1) * page_size
    end = start + page_size + 1  # <-- off-by-one bug
    return items[start:end]
