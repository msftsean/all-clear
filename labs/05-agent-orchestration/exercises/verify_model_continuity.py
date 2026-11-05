#!/usr/bin/env python3
"""Offline participant verifier for model continuity under failover."""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

BACKEND = Path(__file__).resolve().parents[3] / "backend"
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))

from agent_framework import Agent, ChatOptions, Message  # noqa: E402

from app.agents.schemas import EscalationReason, SignalCategory, SignalClassification  # noqa: E402
from app.services.azure.failover_chat_client import (  # noqa: E402
    FailoverChatClient,
    _is_model_unavailable,
    build_failover_client,
)
from app.services.mock.maf_chat_client import MockChatClient  # noqa: E402
from tests.test_failover._fakes import (  # noqa: E402
    RaisingChatClient,
    RecordingChatClient,
    make_named_error,
)


USER = [Message("user", ["building on fire, people may be trapped"])]


async def verify() -> None:
    unavailable = make_named_error("NotFoundError", "DeploymentNotFound", 404)
    primary = RaisingChatClient(unavailable)
    fallback = RecordingChatClient(text="fallback")
    client = FailoverChatClient([primary, fallback], ["primary", "fallback"])
    assert (await client.get_response(USER)).text == "fallback"
    assert client.failover_active and client.last_used_model == "fallback"

    healthy = RecordingChatClient(text="primary")
    untouched = RecordingChatClient(text="fallback")
    healthy_client = FailoverChatClient([healthy, untouched], ["primary", "fallback"])
    assert (await healthy_client.get_response(USER)).text == "primary"
    assert untouched.calls == 0 and not healthy_client.failover_active

    typed = FailoverChatClient(
        [RaisingChatClient(unavailable), MockChatClient()],
        ["primary", "mock-fallback"],
    )
    response = await Agent(typed, instructions="classify").run(
        "Building on fire, people may be trapped",
        options=ChatOptions(response_format=SignalClassification),
    )
    assert isinstance(response.value, SignalClassification)
    assert response.value.intent_category is SignalCategory.PUBLIC_SAFETY
    assert response.value.requires_escalation is True
    assert response.value.escalation_reason is EscalationReason.LIFE_SAFETY

    assert not _is_model_unavailable(
        make_named_error("RateLimitError", "429 Too Many Requests", 429)
    )
    assert not _is_model_unavailable(
        make_named_error("BadRequestError", "content management policy", 400)
    )
    single = RaisingChatClient(unavailable)
    assert build_failover_client([single], ["primary"]) is single


def main() -> int:
    asyncio.run(verify())
    print("PASS: model continuity preserved across failover and safety boundaries")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
