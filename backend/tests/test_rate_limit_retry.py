"""Tests for the Azure OpenAI 429 retry helper (app/agents/retry.py)."""

from __future__ import annotations

import pytest

from app.agents.retry import with_rate_limit_retry

# The helper matches openai's error by type name, so name the class accordingly.
RateLimitError = type("RateLimitError", (Exception,), {})


@pytest.mark.asyncio
async def test_retries_then_succeeds(monkeypatch):
    sleeps: list[float] = []

    async def _fake_sleep(d):
        sleeps.append(d)

    monkeypatch.setattr("app.agents.retry.asyncio.sleep", _fake_sleep)

    calls = {"n": 0}

    async def op():
        calls["n"] += 1
        if calls["n"] < 3:
            raise RateLimitError("Error code: 429 - too_many_requests")
        return "ok"

    result = await with_rate_limit_retry(op)
    assert result == "ok"
    assert calls["n"] == 3
    assert len(sleeps) == 2  # two backoffs before the third (successful) attempt


@pytest.mark.asyncio
async def test_gives_up_after_budget(monkeypatch):
    async def _fake_sleep(d):
        return None

    monkeypatch.setattr("app.agents.retry.asyncio.sleep", _fake_sleep)

    async def op():
        raise RateLimitError("429 Too Many Requests")

    with pytest.raises(RateLimitError):
        await with_rate_limit_retry(op, max_retries=2)


@pytest.mark.asyncio
async def test_non_rate_limit_propagates_immediately():
    calls = {"n": 0}

    async def op():
        calls["n"] += 1
        raise ValueError("nope")

    with pytest.raises(ValueError):
        await with_rate_limit_retry(op)
    assert calls["n"] == 1  # not retried
