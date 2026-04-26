import re


import re

def is_valid_email(email: str) -> bool:
    if email is None or email == "":
        return False
    if email.count("@") != 1:
        return False
    pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z0-9]{2,24}"
    return re.fullmatch(pattern, email) is not None

import re

_EMAIL_RE = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z0-9]{2,24}")

def is_valid_email(email: str) -> bool:
    if not email:
        return False
    if email.count("@") != 1:
        return False
    return re.fullmatch(_EMAIL_RE, email) is not None
