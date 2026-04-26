import httpx


async def fetch_user(user_id: int) -> dict | None:
    """Fetch user from API by ID.

    Args:
        user_id: User ID to fetch

    Returns:
        User data dict on success, None on 404, raises on other errors

    Raises:
        httpx.HTTPStatusError: For 5xx errors
        httpx.TimeoutException: On timeout
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://api.example.com/users/{user_id}")

        if response.status_code == 404:
            return None

        response.raise_for_status()
        return response.json()
