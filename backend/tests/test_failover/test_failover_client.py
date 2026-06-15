"""US1 verifiers: automatic chat-model failover (018-model-agnostic-failover).

Loop Protocol: these verifiers are owned by the tester and are written against the
contract in specs/018-model-agnostic-failover/spec.md. The implementer must not
edit them to make implementation pass.
"""

from __future__ import annotations

import pytest
from agent_framework import Agent, ChatOptions, Message

from app.agents.schemas import EscalationReason, SignalCategory, SignalClassification
from app.services.azure.failover_chat_client import (
    FailoverChatClient,
    _is_model_unavailable,
    build_failover_client,
)
from app.services.mock.maf_chat_client import MockChatClient

from ._fakes import RaisingChatClient, RecordingChatClient, make_named_error

_USER = [Message("user", ["downed power line sparking at 5th & Main"])]


# --- T005: failover advances when the primary is unavailable -----------------

@pytest.mark.parametrize(
    "exc",
    [
        make_named_error("NotFoundError", "DeploymentNotFound: model 'gpt-x' does not exist", 404),
        make_named_error("PermissionDeniedError", "Access denied to deployment", 403),
        make_named_error("AuthenticationError", "Unauthorized", 401),
        make_named_error("APIStatusError", "Service Unavailable", 503),
    ],
)
async def test_failover_advances_on_unavailable(exc) -> None:
    primary = RaisingChatClient(exc)
    fallback = RecordingChatClient(text="served-by-fallback")
    client = FailoverChatClient([primary, fallback], ["primary", "fallback"])

    resp = await client.get_response(_USER)

    assert resp.text == "served-by-fallback"
    assert primary.calls == 1
    assert fallback.calls == 1
    assert client.last_used_model == "fallback"
    assert client.failover_active is True


# --- T006: no failover when the primary is healthy ---------------------------

async def test_no_failover_on_healthy_primary() -> None:
    primary = RecordingChatClient(text="served-by-primary")
    fallback = RecordingChatClient(text="served-by-fallback")
    client = FailoverChatClient([primary, fallback], ["primary", "fallback"])

    resp = await client.get_response(_USER)

    assert resp.text == "served-by-primary"
    assert primary.calls == 1
    assert fallback.calls == 0
    assert client.last_used_model == "primary"
    assert client.failover_active is False


# --- T007: structured output passes through a failover -----------------------

async def test_structured_output_passthrough() -> None:
    primary = RaisingChatClient(make_named_error("NotFoundError", "DeploymentNotFound", 404))
    client = FailoverChatClient([primary, MockChatClient()], ["primary", "mock-fallback"])
    agent = Agent(client, instructions="classify")

    resp = await agent.run(
        "There is a downed power line sparking at 5th & Main, no power on the block",
        options=ChatOptions(response_format=SignalClassification),
    )

    assert isinstance(resp.value, SignalClassification)
    assert client.failover_active is True


# --- T008: no fallback configured is a true no-op ----------------------------

async def test_no_fallback_is_noop() -> None:
    primary = RaisingChatClient(make_named_error("NotFoundError", "DeploymentNotFound", 404))
    # A single-element chain must be returned UNWRAPPED (identical to pre-feature).
    client = build_failover_client([primary], ["primary"])

    assert client is primary
    assert not isinstance(client, FailoverChatClient)
    with pytest.raises(Exception):
        await client.get_response(_USER)


# --- T009: 429 and content-filter are NOT failover triggers ------------------

async def test_rate_limit_is_not_failover() -> None:
    primary = RaisingChatClient(make_named_error("RateLimitError", "429 Too Many Requests", 429))
    fallback = RecordingChatClient()
    client = FailoverChatClient([primary, fallback], ["primary", "fallback"])

    with pytest.raises(Exception):
        await client.get_response(_USER)
    assert fallback.calls == 0


async def test_content_filter_is_not_failover() -> None:
    primary = RaisingChatClient(
        make_named_error(
            "BadRequestError",
            "The response was filtered due to Azure OpenAI's content management policy",
            400,
        )
    )
    fallback = RecordingChatClient()
    client = FailoverChatClient([primary, fallback], ["primary", "fallback"])

    with pytest.raises(Exception):
        await client.get_response(_USER)
    assert fallback.calls == 0


def test_detector_classifies_signals() -> None:
    assert _is_model_unavailable(make_named_error("NotFoundError", "DeploymentNotFound", 404))
    assert _is_model_unavailable(make_named_error("X", "Service Unavailable", 503))
    assert not _is_model_unavailable(make_named_error("RateLimitError", "429", 429))
    assert not _is_model_unavailable(
        make_named_error("X", "filtered due to content management policy", 400)
    )
    assert not _is_model_unavailable(ValueError("some unrelated bug"))


# --- T010: escalation parity holds on the fallback model ---------------------

async def test_escalation_parity_on_fallback() -> None:
    """A SEV1/life-safety signal still escalates when served by the fallback model
    (Constitution Art. III is model-independent)."""
    primary = RaisingChatClient(make_named_error("NotFoundError", "DeploymentNotFound", 404))
    client = FailoverChatClient([primary, MockChatClient()], ["primary", "mock-fallback"])
    agent = Agent(client, instructions="classify")

    resp = await agent.run(
        "Building on fire, people may be trapped on the second floor!",
        options=ChatOptions(response_format=SignalClassification),
    )

    assert isinstance(resp.value, SignalClassification)
    assert resp.value.intent_category is SignalCategory.PUBLIC_SAFETY
    assert resp.value.requires_escalation is True
    assert resp.value.escalation_reason is EscalationReason.LIFE_SAFETY
    assert client.failover_active is True


# --- T011: exhausted chain raises the last error -----------------------------

async def test_chain_exhausted_raises_last_error() -> None:
    first = RaisingChatClient(make_named_error("NotFoundError", "primary DeploymentNotFound", 404))
    second = RaisingChatClient(
        make_named_error("NotFoundError", "fallback DeploymentNotFound", 404)
    )
    client = FailoverChatClient([first, second], ["primary", "fallback"])

    with pytest.raises(Exception) as excinfo:
        await client.get_response(_USER)

    assert "fallback DeploymentNotFound" in str(excinfo.value)
    assert first.calls == 1
    assert second.calls == 1
