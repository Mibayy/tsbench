import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient

from apps.api.main import app
from apps.api.models import User, Order
from apps.api.auth import create_access_token


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def auth_user(db_session):
    user = User(email="buyer@example.com", name="Buyer One", is_active=True)
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def auth_headers(auth_user):
    token = create_access_token({"sub": str(auth_user.id)})
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def mock_send_email():
    with patch("apps.api.services.notifications.send_email") as m:
        m.return_value = MagicMock(message_id="msg_123")
        yield m


def test_orders_api_create_returns_201_and_persists(
    client, db_session, auth_user, auth_headers, mock_send_email
):
    payload = {
        "items": [{"sku": "SKU-1", "qty": 2, "unit_price": "19.99"}],
        "currency": "EUR",
    }

    response = client.post("/api/orders", json=payload, headers=auth_headers)

    assert response.status_code == 201
    body = response.json()
    assert "id" in body
    order_id = body["id"]

    order = db_session.query(Order).filter(Order.id == order_id).one()
    assert order.user_id == auth_user.id
    assert order.currency == "EUR"
    assert len(order.items) == 1

    mock_send_email.assert_called_once()
    call_kwargs = mock_send_email.call_args.kwargs or {}
    to_addr = call_kwargs.get("to") or mock_send_email.call_args.args[0]
    assert to_addr == auth_user.email
    subject = call_kwargs.get("subject", "")
    assert "confirmation" in subject.lower() or "order" in subject.lower()


def test_orders_api_create_unauthenticated_returns_401(client):
    response = client.post("/api/orders", json={"items": []})
    assert response.status_code == 401


@pytest.mark.parametrize(
    "bad_payload,expected_status",
    [
        ({}, 422),
        ({"items": []}, 422),
        ({"items": [{"sku": "X", "qty": 0, "unit_price": "1.00"}]}, 422),
        ({"items": [{"sku": "X", "qty": 1, "unit_price": "-1.00"}]}, 422),
    ],
)
def test_orders_api_create_invalid_payload_rejected(
    client, auth_headers, mock_send_email, bad_payload, expected_status
):
    response = client.post("/api/orders", json=bad_payload, headers=auth_headers)
    assert response.status_code == expected_status
    mock_send_email.assert_not_called()
