"""Bounded retry-with-backoff for Azure OpenAI rate limits (HTTP 429).

The gpt-5.1 deployment has a finite tokens-per-minute budget. A burst of
concurrent signals (many callers/reporters about the same incident, or a load
test) can momentarily exceed it, and Azure OpenAI returns 429 "Too Many
Requests". Agent Framework surfaces that as a ``ChatClientException`` wrapping an
``openai.RateLimitError``; left unhandled it bubbles up as a 500 to the caller.

Real demos rarely hit this (a single human typing / one phone call has no
concurrency), but bursts should degrade gracefully instead of failing. This
helper retries the wrapped coroutine a bounded number of times with jittered
exponential backoff, honoring the server ``Retry-After`` header when present.
"""

from __future__ import annotations

import asyncio
import random
from typing import Awaitable, Callable, TypeVar

T = TypeVar("T")

_MAX_RATE_LIMIT_RETRIES = 5
_BACKOFF_BASE_S = 0.5
_BACKOFF_CAP_S = 8.0


def _is_rate_limit(exc: BaseException) -> bool:
    """True if ``exc`` (or anything in its cause/context chain) is a 429."""
    seen: set[int] = set()
    cur: BaseException | None = exc
    while cur is not None and id(cur) not in seen:
        seen.add(id(cur))
        name = type(cur).__name__
        if name == "RateLimitError":
            return True
        text = str(cur)
        if "429" in text or "too_many_requests" in text or "Too Many Requests" in text:
            return True
        cur = cur.__cause__ or cur.__context__
    return False


def _retry_after_seconds(exc: BaseException) -> float | None:
    """Extract a ``Retry-After`` hint (seconds) from an openai error, if any."""
    cur: BaseException | None = exc
    seen: set[int] = set()
    while cur is not None and id(cur) not in seen:
        seen.add(id(cur))
        response = getattr(cur, "response", None)
        headers = getattr(response, "headers", None)
        if headers is not None:
            value = headers.get("retry-after") or headers.get("Retry-After")
            if value:
                try:
                    return float(value)
                except (TypeError, ValueError):
                    pass
        cur = cur.__cause__ or cur.__context__
    return None


async def with_rate_limit_retry(
    op: Callable[[], Awaitable[T]],
    *,
    max_retries: int = _MAX_RATE_LIMIT_RETRIES,
) -> T:
    """Await ``op()``; on a 429, back off and retry up to ``max_retries`` times.

    ``op`` must be a zero-arg coroutine factory (called fresh each attempt) so the
    underlying request is re-issued rather than re-awaiting a spent coroutine.
    Non-rate-limit errors propagate immediately.
    """
    attempt = 0
    while True:
        try:
            return await op()
        except Exception as exc:  # noqa: BLE001 - re-raised unless it's a 429
            if attempt >= max_retries or not _is_rate_limit(exc):
                raise
            hinted = _retry_after_seconds(exc)
            if hinted is not None:
                delay = hinted + random.uniform(0.0, 0.5)
            else:
                ceiling = min(_BACKOFF_CAP_S, _BACKOFF_BASE_S * (2 ** attempt))
                delay = random.uniform(0.0, ceiling)
            await asyncio.sleep(delay)
            attempt += 1
