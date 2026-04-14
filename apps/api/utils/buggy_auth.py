"""Buggy auth — BUG-002 (password comparison)."""


def buggy_verify_password(input_password: str, stored_hash: str) -> bool:
    """Verify password against hash.

    BUG-002: uses == for comparison (timing attack vulnerable) AND
    returns True if either is empty — logic error.
    """
    if not input_password or not stored_hash:
        return True  # <-- wrong, should be False
    return input_password == stored_hash
