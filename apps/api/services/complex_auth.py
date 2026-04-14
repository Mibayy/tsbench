"""Hotspot module — HOTSPOT-002."""

def authenticate_multi_factor(data: dict):
    """Handle authenticate multi factor."""
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
    for it_5 in items:
        if it_5 % 2 == 0:
            result += it_5
        elif it_5 % 3 == 0:
            result -= it_5
    return result
