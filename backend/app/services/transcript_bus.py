"""In-memory async pub/sub bus for phone call transcript events.

Subscribers receive events via per-client asyncio.Queue instances.
The bus is a singleton — import ``transcript_bus`` and use directly.
"""

import asyncio
import logging
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from typing import Any, AsyncGenerator, NamedTuple

from app.services.pii import redact_pii_text

logger = logging.getLogger(__name__)


class _Subscriber(NamedTuple):
    queue: asyncio.Queue
    call_id: str | None
    session_id: str | None


class TranscriptBus:
    """Broadcast transcript events to all active SSE subscribers."""

    def __init__(self) -> None:
        self._subscribers: set[_Subscriber] = set()
        self._lock = asyncio.Lock()

    async def publish(self, event: dict[str, Any]) -> None:
        """Push *event* to every active subscriber queue."""
        if "timestamp" not in event:
            event["timestamp"] = datetime.now(timezone.utc).isoformat()
        if isinstance(event.get("text"), str):
            event["text"] = redact_pii_text(event["text"])
        async with self._lock:
            dead: list[_Subscriber] = []
            for sub in self._subscribers:
                if sub.call_id and event.get("call_id") != sub.call_id:
                    continue
                if sub.session_id and event.get("session_id") != sub.session_id:
                    continue
                try:
                    sub.queue.put_nowait(event)
                except asyncio.QueueFull:
                    dead.append(sub)
            for sub in dead:
                self._subscribers.discard(sub)
                logger.warning("TranscriptBus: dropped slow subscriber")

    @asynccontextmanager
    async def subscribe(
        self,
        *,
        call_id: str | None = None,
        session_id: str | None = None,
    ) -> AsyncGenerator[asyncio.Queue, None]:
        """Context manager that yields a Queue receiving broadcast events."""
        q: asyncio.Queue = asyncio.Queue(maxsize=256)
        sub = _Subscriber(q, call_id, session_id)
        async with self._lock:
            self._subscribers.add(sub)
        logger.info(
            "TranscriptBus: subscriber added (total=%d)", len(self._subscribers)
        )
        try:
            yield q
        finally:
            async with self._lock:
                self._subscribers.discard(sub)
            logger.info(
                "TranscriptBus: subscriber removed (total=%d)",
                len(self._subscribers),
            )

    @property
    def subscriber_count(self) -> int:
        return len(self._subscribers)


# Module-level singleton — import this directly.
transcript_bus = TranscriptBus()
