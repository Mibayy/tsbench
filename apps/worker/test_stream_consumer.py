import pytest
from unittest.mock import Mock, call
from stream_consumer import consume


def test_consume_creates_group_with_mkstream():
    """XGROUP CREATE should be called with MKSTREAM flag"""
    redis_mock = Mock()
    redis_mock.xreadgroup.return_value = None

    # Start consumer in a controlled way
    consumer = consume(
        redis_mock,
        stream="test-stream",
        group="test-group",
        consumer_name="consumer-1",
        handler=Mock(),
    )

    # Verify group creation
    redis_mock.xgroup_create.assert_called_once_with(
        name="test-stream",
        groupname="test-group",
        id="0",
        mkstream=True,
    )


def test_consume_ignores_busygroup_error():
    """BUSYGROUP error should be ignored (group already exists)"""
    redis_mock = Mock()
    redis_mock.xgroup_create.side_effect = Exception("BUSYGROUP Consumer group 'test-group' already exists")
    redis_mock.xreadgroup.return_value = None
    handler_mock = Mock()

    # Should not raise
    consume(
        redis_mock,
        stream="test-stream",
        group="test-group",
        consumer_name="consumer-1",
        handler=handler_mock,
    )


def test_consume_calls_handler_on_message():
    """Handler should be called with msg_id and data"""
    redis_mock = Mock()
    redis_mock.xgroup_create.side_effect = Exception("BUSYGROUP")

    msg_id = b"1234567890-0"
    msg_data = {b"key": b"value"}
    redis_mock.xreadgroup.return_value = [(b"test-stream", [(msg_id, msg_data)])]

    handler_mock = Mock()

    consume(
        redis_mock,
        stream="test-stream",
        group="test-group",
        consumer_name="consumer-1",
        handler=handler_mock,
    )

    handler_mock.assert_called_once_with(msg_id, msg_data)


def test_consume_acks_on_handler_success():
    """XACK should be called after successful handler execution"""
    redis_mock = Mock()
    redis_mock.xgroup_create.side_effect = Exception("BUSYGROUP")

    msg_id = b"1234567890-0"
    msg_data = {b"key": b"value"}
    redis_mock.xreadgroup.return_value = [(b"test-stream", [(msg_id, msg_data)])]

    handler_mock = Mock()

    consume(
        redis_mock,
        stream="test-stream",
        group="test-group",
        consumer_name="consumer-1",
        handler=handler_mock,
    )

    redis_mock.xack.assert_called_once_with("test-stream", "test-group", msg_id)


def test_consume_no_xack_on_handler_exception(caplog):
    """XACK should NOT be called if handler raises; exception should be logged"""
    redis_mock = Mock()
    redis_mock.xgroup_create.side_effect = Exception("BUSYGROUP")

    msg_id = b"1234567890-0"
    msg_data = {b"key": b"value"}
    redis_mock.xreadgroup.return_value = [(b"test-stream", [(msg_id, msg_data)])]

    handler_mock = Mock()
    handler_mock.side_effect = ValueError("Handler failed")

    consume(
        redis_mock,
        stream="test-stream",
        group="test-group",
        consumer_name="consumer-1",
        handler=handler_mock,
    )

    # XACK should NOT be called
    redis_mock.xack.assert_not_called()

    # Exception should be logged
    assert "handler failed for msg_id" in caplog.text


def test_consume_respects_block_ms():
    """block_ms parameter should be passed to XREADGROUP"""
    redis_mock = Mock()
    redis_mock.xgroup_create.side_effect = Exception("BUSYGROUP")
    redis_mock.xreadgroup.return_value = None

    consume(
        redis_mock,
        stream="test-stream",
        group="test-group",
        consumer_name="consumer-1",
        handler=Mock(),
        block_ms=10000,
    )

    # Verify block parameter
    call_args = redis_mock.xreadgroup.call_args
    assert call_args[1]["block"] == 10000
