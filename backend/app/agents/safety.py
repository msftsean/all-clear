"""Runtime safety net shared by the text and voice pipelines."""
from __future__ import annotations

from app.agents.escalation_rules import contains_harm_signal
from app.agents.schemas import ActionStatus, EscalationReason, Queue, Severity

CRISIS_MESSAGE = (
    "It sounds like you may be going through something serious, and you deserve "
    "immediate human support. If you are in immediate danger, call local "
    "emergency services. In the U.S. or Canada, call or text 988 for crisis support."
)


def apply_safety_override(message: str) -> dict | None:
    """Return escalation metadata when ``message`` carries a harm signal.

    The result is intent-independent: it fires purely on harm-signal detection,
    so a mis-classified or adversarially spoofed intent can never suppress a
    crisis escalation. Returns ``None`` when no harm signal is present, letting
    the caller continue its normal pipeline.
    """
    if not contains_harm_signal(message):
        return None
    return {
        "queue": Queue.ESCALATIONS,
        "status": ActionStatus.ESCALATED,
        "escalation_reason": EscalationReason.SENTIMENT_SAFETY,
        "severity": Severity.SEV1,
        "escalated": True,
        "safety_override": True,
        "message": CRISIS_MESSAGE,
    }


def _any_string_has_harm(value: object) -> bool:
    """Recursively check every string within a JSON-like value for a harm signal."""
    if isinstance(value, str):
        return contains_harm_signal(value)
    if isinstance(value, dict):
        return any(_any_string_has_harm(v) for v in value.values())
    if isinstance(value, (list, tuple)):
        return any(_any_string_has_harm(v) for v in value)
    return False


def voice_crisis_result(arguments: dict) -> dict | None:
    """Intent-independent crisis override for voice tool calls.

    Recursively scans ALL string values in the tool arguments (not just
    ``query``/``reason``/``message``) for a harm signal. If found, returns an
    escalation payload (no KB articles) to be serialized as the tool result for
    ANY tool — including ``search_knowledge_base`` — so a crisis utterance can
    never be answered with self-service content. Returns ``None`` otherwise.
    """
    if _any_string_has_harm(arguments):
        return {
            "intent": "human_escalation",
            "queue": Queue.ESCALATIONS.value,
            "confidence": 1.0,
            "requires_escalation": True,
            "escalated": True,
            "safety_override": True,
            "severity": Severity.SEV1.value,
            "message": CRISIS_MESSAGE,
            "articles": [],
        }
    return None
