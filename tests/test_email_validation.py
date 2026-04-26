import pytest

from packages.utils.validate_email import is_valid_email


@pytest.mark.parametrize(
    "email,expected",
    [
        pytest.param("user@example.com", True, id="simple"),
        pytest.param("first.last@example.com", True, id="dot-in-local"),
        pytest.param("user+tag@example.co", True, id="plus-tag"),
        pytest.param("u_s-er%99@sub.example.org", True, id="special-chars-and-subdomain"),
        pytest.param("a@b.io", True, id="short-tld-2-chars"),
        pytest.param("USER@EXAMPLE.COM", True, id="uppercase"),
        pytest.param("", False, id="empty-string"),
        pytest.param("plainaddress", False, id="missing-at"),
        pytest.param("user@@example.com", False, id="double-at"),
        pytest.param("user@example", False, id="missing-tld-dot"),
        pytest.param("user@example.c", False, id="tld-too-short"),
        pytest.param("user name@example.com", False, id="space-in-local"),
    ],
)
def test_is_valid_email_parametrize(email, expected):
    assert is_valid_email(email) is expected
