"""Runtime safety net shared by the text and voice pipelines.

Wraps the hardened, intent-INDEPENDENT crisis detection in
``app.agents.escalation_rules`` so a single source of truth forces human
escalation on harm signals regardless of how the intent classifier labels a
message. Returns app-native enum fields ready for ``ChatResponse``, ticket, and
audit-log construction (no raw scenario strings leak into the runtime).
"""
from __future__ import annotations

from app.agents.escalation_rules import contains_harm_signal
from app.models.enums import ActionStatus, Department, EscalationReason, Priority

CRISIS_MESSAGE = (
    "It sounds like you may be going through something serious, and you deserve "
    "to talk to a real person right now. I'm connecting you with a counselor. "
    "If you are in immediate danger, call 911 or campus safety. You can also "
    "reach the 988 Suicide & Crisis Lifeline by calling or texting 988."
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
        "department": Department.ESCALATE_TO_HUMAN,
        "status": ActionStatus.ESCALATED,
        "escalation_reason": EscalationReason.SENSITIVE_TOPIC,
        "priority": Priority.URGENT,
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
            "department": "ESCALATE_TO_HUMAN",
            "confidence": 1.0,
            "requires_escalation": True,
            "escalated": True,
            "safety_override": True,
            "priority": "urgent",
            "message": CRISIS_MESSAGE,
            "articles": [],
        }
    return None
