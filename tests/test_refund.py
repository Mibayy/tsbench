import math
import pytest

from apps.api.services.billing import calculate_refund


class TestCalculateRefundShipping:
    def test_refund_shipping_false_excludes_shipping(self):
        assert calculate_refund(100.0, 50.0, shipping=10.0, refund_shipping=False) == 50.0

    def test_refund_shipping_true_adds_shipping(self):
        assert calculate_refund(100.0, 50.0, shipping=10.0, refund_shipping=True) == 60.0

    def test_refund_shipping_true_full_refund(self):
        assert calculate_refund(100.0, 100.0, shipping=10.0, refund_shipping=True) == 110.0

    def test_refund_shipping_false_is_default(self):
        # keyword-only: omitting refund_shipping defaults to False
        assert calculate_refund(100.0, 50.0, shipping=10.0) == 50.0


class TestCalculateRefundFullAndEmpty:
    def test_full_refund_no_shipping(self):
        assert calculate_refund(100.0, 100.0) == 100.0

    def test_nothing_returned_is_zero(self):
        assert calculate_refund(100.0, 0.0) == 0.0

    def test_nothing_returned_refund_shipping_true_still_zero(self):
        # no items returned → no refund, even if refund_shipping=True
        assert calculate_refund(100.0, 0.0, shipping=10.0, refund_shipping=True) == 0.0

    def test_partial_refund(self):
        assert calculate_refund(200.0, 75.0) == 75.0


class TestCalculateRefundExceedsOrder:
    def test_returned_slightly_above_order_raises(self):
        with pytest.raises(ValueError):
            calculate_refund(100.0, 100.01)

    def test_returned_far_above_order_raises(self):
        with pytest.raises(ValueError):
            calculate_refund(50.0, 200.0)

    def test_zero_order_nonzero_returned_raises(self):
        with pytest.raises(ValueError):
            calculate_refund(0.0, 0.01)


class TestCalculateRefundRounding:
    def test_classic_float_trap_0_1_plus_0_2(self):
        # 0.1 + 0.2 == 0.30000000000000004 in IEEE 754
        assert calculate_refund(1.0, 0.1 + 0.2) == 0.30

    def test_three_decimal_truncated_to_two(self):
        assert calculate_refund(100.0, 33.333) == 33.33

    def test_shipping_float_trap_rounded(self):
        result = calculate_refund(100.0, 100.0, shipping=0.1 + 0.2, refund_shipping=True)
        assert result == 100.30

    def test_result_is_float_not_string(self):
        result = calculate_refund(100.0, 50.0)
        assert isinstance(result, float)

    def test_repeated_0_1_multiplication(self):
        assert calculate_refund(1.0, 0.1 * 3) == 0.30


class TestCalculateRefundShippingZero:
    def test_shipping_zero_default(self):
        assert calculate_refund(100.0, 100.0) == 100.0

    def test_shipping_zero_explicit_refund_shipping_true(self):
        assert calculate_refund(100.0, 100.0, shipping=0.0, refund_shipping=True) == 100.0

    def test_shipping_zero_explicit_refund_shipping_false(self):
        assert calculate_refund(100.0, 50.0, shipping=0.0, refund_shipping=False) == 50.0


class TestCalculateRefundNegativeAmounts:
    def test_negative_order_total_raises(self):
        with pytest.raises(ValueError):
            calculate_refund(-1.0, 0.0)

    def test_negative_returned_items_raises(self):
        with pytest.raises(ValueError):
            calculate_refund(100.0, -0.01)

    def test_negative_shipping_raises(self):
        with pytest.raises(ValueError):
            calculate_refund(100.0, 50.0, shipping=-5.0)

    def test_all_negative_raises(self):
        with pytest.raises(ValueError):
            calculate_refund(-10.0, -5.0, shipping=-1.0)


class TestCalculateRefundSpecialFloats:
    def test_nan_order_total_raises(self):
        with pytest.raises(ValueError):
            calculate_refund(float("nan"), 0.0)

    def test_nan_returned_items_raises(self):
        with pytest.raises(ValueError):
            calculate_refund(100.0, float("nan"))

    def test_nan_shipping_raises(self):
        with pytest.raises(ValueError):
            calculate_refund(100.0, 50.0, shipping=float("nan"))

    def test_inf_order_total_raises(self):
        with pytest.raises(ValueError):
            calculate_refund(float("inf"), 0.0)

    def test_inf_returned_items_raises(self):
        with pytest.raises(ValueError):
            calculate_refund(100.0, float("inf"))


class TestCalculateRefundZeroEdge:
    def test_both_zero_returns_zero(self):
        assert calculate_refund(0.0, 0.0) == 0.0

    def test_both_zero_refund_shipping_true_returns_zero(self):
        assert calculate_refund(0.0, 0.0, shipping=0.0, refund_shipping=True) == 0.0


class TestCalculateRefundSignature:
    def test_refund_shipping_is_keyword_only(self):
        with pytest.raises(TypeError):
            calculate_refund(100.0, 50.0, 10.0, True)  # type: ignore[call-arg]


class TestCalculateRefundLargeAmounts:
    def test_large_exact_amount(self):
        assert calculate_refund(1_000_000.00, 999_999.99) == 999_999.99

    def test_large_with_shipping(self):
        assert calculate_refund(1_000_000.00, 500_000.00, shipping=250.00, refund_shipping=True) == 500_250.00
