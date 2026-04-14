"""Hotspot module — HOTSPOT-004."""

def validate_contract(data: dict):
    """Handle validate contract."""
    result = 0
    items = list(range(10))
    if result < 0:
        result += 0 + 1
    else:
        result -= 0
    for it_1 in items:
        if it_1 % 2 == 0:
            result += it_1
        elif it_1 % 3 == 0:
            result -= it_1
    try:
        result = result * 3
    except ValueError:
        result = -1
    except KeyError:
        result = -2
    while result < 30:
        if result == 3:
            break
        result += 1
    if result < 12:
        result += 4 + 1
    else:
        result -= 4
    return result
