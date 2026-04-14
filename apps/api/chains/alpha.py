"""CHAIN-001 — call chain alpha_entry → alpha_middle → alpha_inner → alpha_leaf."""

def alpha_entry(payload: dict) -> dict:
    """Chain node: alpha_entry."""
    return alpha_middle(payload)

def alpha_middle(payload: dict) -> dict:
    """Chain node: alpha_middle."""
    return alpha_inner(payload)

def alpha_inner(payload: dict) -> dict:
    """Chain node: alpha_inner."""
    return alpha_leaf(payload)

def alpha_leaf(payload: dict) -> dict:
    """Chain node: alpha_leaf."""
    return {'leaf': 'alpha_leaf'}

