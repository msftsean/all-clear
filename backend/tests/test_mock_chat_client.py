"""Tests for the mock MAF chat client (001-maf-rehost, T3)."""

from agent_framework import Agent, ChatOptions

from app.agents.schemas import (
    EscalationReason,
    Queue,
    Sentiment,
    SignalCategory,
    SignalClassification,
)
from app.services.mock.maf_chat_client import MockChatClient, classify_signal, detect_pii


async def test_agent_run_returns_typed_value() -> None:
    """agent.run against the mock returns a typed SignalClassification via .value."""
    agent = Agent(MockChatClient(), instructions="classify")
    resp = await agent.run(
        "There is a downed power line sparking at 5th & Main, no power on the block",
        options=ChatOptions(response_format=SignalClassification),
    )
    assert isinstance(resp.value, SignalClassification)
    assert resp.value.target_queue in (Queue.FIELD_OPERATIONS, Queue.ENGINEERING)
    assert resp.value.entities.severity_indicators


async def test_plain_text_without_response_format() -> None:
    agent = Agent(MockChatClient(), instructions="chat")
    resp = await agent.run("hello")
    assert resp.value is None or isinstance(resp.value, str) or resp.text


def test_classifier_public_safety_escalates() -> None:
    c = classify_signal("Building fire with people trapped inside, immediately!")
    assert c.intent_category is SignalCategory.PUBLIC_SAFETY
    assert c.requires_escalation is True
    assert c.escalation_reason is EscalationReason.LIFE_SAFETY
    assert c.sentiment is Sentiment.URGENT


def test_classifier_customer_inquiry() -> None:
    c = classify_signal("Question about my bill, when will I get a refund?")
    assert c.intent_category is SignalCategory.CUSTOMER_INQUIRY
    assert c.target_queue is Queue.CUSTOMER_COMMS
    assert c.requires_escalation is False


def test_classifier_human_request() -> None:
    c = classify_signal("I want to speak to a human representative")
    assert c.requires_escalation is True
    assert c.escalation_reason is EscalationReason.USER_REQUESTED_HUMAN


def test_pii_detection_flags_but_classifies() -> None:
    c = classify_signal("My SSN is 123-45-6789 and email a@b.com, power outage on my street")
    assert c.pii_detected is True
    assert "ssn" in c.pii_types and "email" in c.pii_types


def test_detect_pii_phone() -> None:
    found, types = detect_pii("call me at (555) 123-4567")
    assert found and "phone" in types


def test_determinism() -> None:
    text = "transformer blew, no power, sparks everywhere on Oak Ave"
    assert classify_signal(text).model_dump() == classify_signal(text).model_dump()
