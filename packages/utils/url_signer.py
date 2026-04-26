import hmac
import hashlib
import time
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse


def sign_url(url: str, secret: str, expires_in: int = 3600) -> str:
    """Sign a URL with HMAC-SHA256."""
    exp = int(time.time()) + expires_in
    parsed = urlparse(url)
    query_params = dict(parse_qsl(parsed.query))
    query_params.pop("sig", None)
    query_params.pop("exp", None)

    base = urlunparse(parsed._replace(query=urlencode(query_params)))
    payload = f"{base}{exp}"
    sig = hmac.new(secret.encode(), payload.encode(), hashlib.sha256).hexdigest()

    query_params["exp"] = str(exp)
    query_params["sig"] = sig
    return urlunparse(parsed._replace(query=urlencode(query_params)))


def verify_signed_url(signed_url: str, secret: str) -> bool:
    """Verify a signed URL."""
    parsed = urlparse(signed_url)
    query_params = dict(parse_qsl(parsed.query))

    sig = query_params.pop("sig", None)
    exp_str = query_params.pop("exp", None)
    if sig is None or exp_str is None:
        return False

    try:
        exp = int(exp_str)
    except ValueError:
        return False

    if exp <= int(time.time()):
        return False

    base = urlunparse(parsed._replace(query=urlencode(query_params)))
    payload = f"{base}{exp}"
    expected = hmac.new(secret.encode(), payload.encode(), hashlib.sha256).hexdigest()

    return hmac.compare_digest(sig, expected)
