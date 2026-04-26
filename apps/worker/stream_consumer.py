"""Redis Streams consumer worker."""
from __future__ import annotations

import logging
from typing import Callable

log = logging.getLogger(__name__)


from redis.exceptions import BusyGroupError

logger = logging.getLogger(__name__)


def consume(redis_client, stream: str, group: str, consumer_name: str, handler, *, block_ms: int = 5000):
    try:
        redis_client.xgroup_create(stream, group, id="0", mkstream=True)
    except Exception as e:
        if "BUSYGROUP" not in str(e):
            raise

    while True:
        resp = redis_client.xreadgroup(
            group, consumer_name, {stream: ">"}, count=10, block=block_ms
        )
        if not resp:
            continue
        for _stream_name, messages in resp:
            for msg_id, data in messages:
                try:
                    handler(msg_id, data)
                    redis_client.xack(stream, group, msg_id)
                except Exception:
                    logger.exception(
                        "handler failed for msg_id=%s on stream=%s group=%s; leaving in PEL for retry",
                        msg_id, stream, group,
                    )
