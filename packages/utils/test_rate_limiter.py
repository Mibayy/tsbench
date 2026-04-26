import time
import pytest
from rate_limiter import TokenBucket


def test_consume_available_tokens():
    """Consume returns True when tokens available."""
    bucket = TokenBucket(capacity=10, refill_rate=1.0)
    assert bucket.consume(5) is True
    assert bucket.tokens == 5.0


def test_consume_insufficient_tokens():
    """Consume returns False when tokens unavailable."""
    bucket = TokenBucket(capacity=5, refill_rate=1.0)
    assert bucket.consume(10) is False
    assert bucket.tokens == 5.0


def test_lazy_refill():
    """Tokens refill lazily based on elapsed time."""
    bucket = TokenBucket(capacity=10, refill_rate=1.0)
    bucket.consume(9)  # 1 token left
    time.sleep(0.1)
    assert bucket.consume(1) is True  # +0.1 tokens from refill


def test_refill_capped_at_capacity():
    """Refilled tokens capped at capacity."""
    bucket = TokenBucket(capacity=10, refill_rate=1.0)
    bucket.consume(5)  # 5 tokens left
    time.sleep(10)  # Would refill 10, but capped at capacity
    bucket.consume(0)  # Trigger lazy refill without consuming
    assert bucket.tokens == 10.0


def test_consume_exact_tokens():
    """Consume exactly available tokens."""
    bucket = TokenBucket(capacity=5, refill_rate=0.0)
    assert bucket.consume(5) is True
    assert bucket.tokens == 0.0
    assert bucket.consume(1) is False


def test_multiple_consumes():
    """Multiple consumes drain tokens correctly."""
    bucket = TokenBucket(capacity=10, refill_rate=0.0)
    assert bucket.consume(2) is True
    assert bucket.consume(3) is True
    assert bucket.consume(5) is True
    assert bucket.consume(1) is False
