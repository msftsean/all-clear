"""In-memory async pub/sub bus for phone call transcript events.

Subscribers receive events via per-client asyncio.Queue instances.
The bus is a singleton — import ``transcript_bus`` and use directly.
"""

import asyncio
import logging
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from typing import Any, AsyncGenerator

from app.services.pii import redact_pii

logger = logging.getLogger(__name__)


class TranscriptBus:
    """Broadcast transcript events to all active SSE subscribers."""

    def __init__(self) -> None:
        self._subscribers: dict[asyncio.Queue, str | None] = {}
        self._lock = asyncio.Lock()

    async def publish(self, event: dict[str, Any]) -> None:
        """Redact PII, then deliver to matching subscribers."""
        safe_event = redact_pii(event)
        if "timestamp" not in safe_event:
            safe_event["timestamp"] = datetime.now(timezone.utc).isoformat()
        async with self._lock:
            dead: list[asyncio.Queue] = []
            for q, subscribed_call_id in self._subscribers.items():
                if (
                    subscribed_call_id is not None
                    and safe_event.get("call_id") != subscribed_call_id
                ):
                    continue
                try:
                    q.put_nowait(safe_event)
                except asyncio.QueueFull:
                    dead.append(q)
            for q in dead:
                self._subscribers.pop(q, None)
                logger.warning("TranscriptBus: dropped slow subscriber")

    @asynccontextmanager
    async def subscribe(
        self,
        call_id: str | None = None,
    ) -> AsyncGenerator[asyncio.Queue, None]:
        """Yield all internal events or only events for one server-known call."""
        q: asyncio.Queue = asyncio.Queue(maxsize=256)
        async with self._lock:
            self._subscribers[q] = call_id
        logger.info(
            "TranscriptBus: subscriber added (total=%d)", len(self._subscribers)
        )
        try:
            yield q
        finally:
            async with self._lock:
                self._subscribers.pop(q, None)
            logger.info(
                "TranscriptBus: subscriber removed (total=%d)",
                len(self._subscribers),
            )

    @property
    def subscriber_count(self) -> int:
        return len(self._subscribers)


# Module-level singleton — import this directly.
transcript_bus = TranscriptBus()
