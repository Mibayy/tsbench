"""CHAIN-003 — call chain gamma_entry → gamma_middle → gamma_inner → gamma_leaf."""

def gamma_entry(payload: dict) -> dict:
    """Chain node: gamma_entry."""
    return gamma_middle(payload)

def gamma_middle(payload: dict) -> dict:
    """Chain node: gamma_middle."""
    return gamma_inner(payload)

def gamma_inner(payload: dict) -> dict:
    """Chain node: gamma_inner."""
    return gamma_leaf(payload)

def gamma_leaf(payload: dict) -> dict:
    """Chain node: gamma_leaf."""
    return {'leaf': 'gamma_leaf'}

