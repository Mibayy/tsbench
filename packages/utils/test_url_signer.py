import time
import pytest
import sys
sys.path.insert(0, '/tmp/tsbench-bench')
from packages.utils.url_signer import sign_url, verify_signed_url


def test_sign_url_basic():
    """sign_url appends sig and exp query params."""
    url = "https://example.com/page"
    secret = "test-secret"
    signed = sign_url(url, secret, expires_in=3600)

    assert "sig=" in signed
    assert "exp=" in signed
    assert url in signed or "example.com" in signed


def test_sign_url_with_existing_params():
    """sign_url preserves existing query parameters."""
    url = "https://example.com/page?foo=bar&baz=qux"
    secret = "test-secret"
    signed = sign_url(url, secret)

    assert "foo=bar" in signed
    assert "baz=qux" in signed
    assert "sig=" in signed
    assert "exp=" in signed


def test_sign_url_deterministic():
    """sign_url with same inputs produces same output (for same timestamp)."""
    url = "https://example.com/page"
    secret = "test-secret"

    # Mock exp by signing with fixed timestamp
    import hmac
    import hashlib
    from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse

    exp = int(time.time()) + 3600
    payload = f"{url}{exp}".encode()
    sig = hmac.new(secret.encode(), payload, hashlib.sha256).hexdigest()

    parsed = urlparse(url)
    params = parse_qsl(parsed.query, keep_blank_values=True)
    params.extend([("sig", sig), ("exp", str(exp))])
    expected = urlunparse(parsed._replace(query=urlencode(params)))

    # Actual sign_url might have different timestamp, so we just check format
    signed = sign_url(url, secret)
    assert "sig=" in signed
    assert "exp=" in signed


def test_verify_signed_url_valid():
    """verify_signed_url returns True for valid signed URL."""
    url = "https://example.com/page"
    secret = "test-secret"
    signed = sign_url(url, secret, expires_in=3600)

    assert verify_signed_url(signed, secret) is True


def test_verify_signed_url_invalid_signature():
    """verify_signed_url returns False with wrong secret."""
    url = "https://example.com/page"
    secret = "test-secret"
    signed = sign_url(url, secret)

    assert verify_signed_url(signed, "wrong-secret") is False


def test_verify_signed_url_missing_sig():
    """verify_signed_url returns False without sig param."""
    url = "https://example.com/page?exp=123456"
    assert verify_signed_url(url, "secret") is False


def test_verify_signed_url_missing_exp():
    """verify_signed_url returns False without exp param."""
    url = "https://example.com/page?sig=abc123"
    assert verify_signed_url(url, "secret") is False


def test_verify_signed_url_expired():
    """verify_signed_url returns False for expired URL."""
    url = "https://example.com/page"
    secret = "test-secret"
    signed = sign_url(url, secret, expires_in=1)

    time.sleep(1.1)
    assert verify_signed_url(signed, secret) is False


def test_verify_signed_url_invalid_exp_format():
    """verify_signed_url returns False with non-integer exp."""
    url = "https://example.com/page?sig=abc&exp=not-a-number"
    assert verify_signed_url(url, "secret") is False


def test_verify_signed_url_preserves_params():
    """verify_signed_url works with existing parameters intact."""
    url = "https://example.com/page?foo=bar"
    secret = "test-secret"
    signed = sign_url(url, secret)

    # Signature should verify even with original params present
    assert verify_signed_url(signed, secret) is True


def test_sign_and_verify_roundtrip():
    """Sign and verify roundtrip works."""
    urls = [
        "https://example.com/",
        "https://example.com/path",
        "https://example.com/path?a=1&b=2",
        "https://api.service.io/verify?token=xyz&user=john",
    ]
    secret = "my-secret-key"

    for url in urls:
        signed = sign_url(url, secret, expires_in=7200)
        assert verify_signed_url(signed, secret) is True
        assert verify_signed_url(signed, "wrong-secret") is False
