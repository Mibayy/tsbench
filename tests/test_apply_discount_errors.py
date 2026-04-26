"""Error-path tests for apps/api/services/billing.py::apply_discount."""
import pytest
from unittest.mock import patch

from apps.api.services.billing import apply_discount
from apps.api.utils.errors import ValidationError


def test_missing_discount_percent_raises():
    with pytest.raises(ValidationError, match="discount_percent is required"):
        apply_discount({}, user_id=1)


def test_negative_discount_percent_raises():
    with pytest.raises(ValidationError, match="discount_percent must be between 0 and 100"):
        apply_discount({"discount_percent": -1}, user_id=1)


def test_discount_percent_above_100_raises():
    with pytest.raises(ValidationError, match="discount_percent must be between 0 and 100"):
        apply_discount({"discount_percent": 101}, user_id=1)


def test_discount_percent_non_numeric_raises():
    # str triggers TypeError on comparison operators (< / >)
    with pytest.raises((ValidationError, TypeError)):
        apply_discount({"discount_percent": "abc"}, user_id=1)


def test_discount_percent_none_is_treated_as_missing():
    # None is caught by the `is None` guard → same as missing key
    with pytest.raises(ValidationError, match="discount_percent is required"):
        apply_discount({"discount_percent": None}, user_id=1)


@pytest.mark.xfail(reason="no negative-user-id business rule implemented yet", strict=True)
def test_negative_user_id_raises():
    with pytest.raises(ValidationError):
        apply_discount({"discount_percent": 10}, user_id=-1)


def test_db_down_propagates_exception():
    with patch(
        "apps.api.services.billing._billing_admin_db",
        side_effect=ConnectionError("db down"),
    ):
        with pytest.raises(ConnectionError):
            apply_discount({"discount_percent": 10}, user_id=1)


def test_payload_not_dict_raises():
    # str has no .get() method → AttributeError
    with pytest.raises(AttributeError):
        apply_discount("not-a-dict", user_id=1)
