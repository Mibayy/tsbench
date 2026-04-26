import httpx
import pytest
import respx

from app.users import fetch_user


@pytest.mark.asyncio
@respx.mock
async def test_fetch_user_success():
    """200 response returns user data."""
    payload = {"id": 1, "name": "Alice"}
    respx.get("https://api.example.com/users/1").mock(
        return_value=httpx.Response(200, json=payload)
    )
    result = await fetch_user(1)
    assert result == payload


@pytest.mark.asyncio
@respx.mock
async def test_fetch_user_not_found_returns_none():
    """404 response returns None."""
    respx.get("https://api.example.com/users/42").mock(
        return_value=httpx.Response(404)
    )
    result = await fetch_user(42)
    assert result is None


@pytest.mark.asyncio
@respx.mock
async def test_fetch_user_server_error_raises():
    """500 response raises HTTPStatusError."""
    respx.get("https://api.example.com/users/7").mock(
        return_value=httpx.Response(500)
    )
    with pytest.raises(httpx.HTTPStatusError):
        await fetch_user(7)


@pytest.mark.asyncio
@respx.mock
async def test_fetch_user_timeout_raises():
    """Timeout raises httpx.TimeoutException."""
    respx.get("https://api.example.com/users/9").mock(
        side_effect=httpx.TimeoutException("timeout")
    )
    with pytest.raises(httpx.TimeoutException):
        await fetch_user(9)
