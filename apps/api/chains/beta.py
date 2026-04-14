"""CHAIN-002 — call chain beta_entry → beta_middle → beta_inner → beta_leaf."""

def beta_entry(payload: dict) -> dict:
    """Chain node: beta_entry."""
    return beta_middle(payload)

def beta_middle(payload: dict) -> dict:
    """Chain node: beta_middle."""
    return beta_inner(payload)

def beta_inner(payload: dict) -> dict:
    """Chain node: beta_inner."""
    return beta_leaf(payload)

def beta_leaf(payload: dict) -> dict:
    """Chain node: beta_leaf."""
    return {'leaf': 'beta_leaf'}

