"""CYCLE-002 part Z."""
from apps.api.cycles import mod_x


def z_call():
    """Z calls X."""
    return mod_x.x_call()
