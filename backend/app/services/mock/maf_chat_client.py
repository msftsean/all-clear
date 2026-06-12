"""
Mock MAF chat client for All Clear (001-maf-rehost, T3).

A BaseChatClient twin (plan.md Appendix B) that runs the full pipeline offline.
When ChatOptions carry a ``response_format`` (the only structured-output agent is
QueryAgent -> SignalClassification), it returns a ChatResponse whose ``.value`` is
a conformant, keyword-derived classification. With no response_format it returns
a plain assistant message.

Mock and live stay in lockstep: this client is selected by core.dependencies when
USE_MOCK_MODE=true (Constitution Art. V). The keyword classifier here is the mock
"model"; it is deliberately deterministic so the surge replay and the labeled eval
set behave identically on every run.
"""

from __future__ import annotations

import re
from typing import Any, Mapping, Optional, Sequence

from pydantic import BaseModel

from agent_framework import BaseChatClient, ChatResponse, Message

from app.agents.schemas import (
    EscalationReason,
    Queue,
    Sentiment,
    SignalCategory,
    SignalClassification,
    SignalEntities,
)

# --- PII patterns (CONTEXT.md / Constitution Art. I: detect, never echo) ---
_SSN_RE = re.compile(r"\b\d{3}-\d{2}-\d{4}\b")
_EMAIL_RE = re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b")
_PHONE_RE = re.compile(r"\b(?:\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b")

# --- Keyword -> (category, queue) routing hints ---
_CATEGORY_KEYWORDS: list[tuple[SignalCategory, Queue, tuple[str, ...]]] = [
    (
        SignalCategory.PUBLIC_SAFETY,
        Queue.FIELD_OPERATIONS,
        ("fire", "smoke", "gas leak", "injured", "trapped", "explosion", "collapse", "unconscious", "bleeding"),
    ),
    (
        SignalCategory.FIELD_HAZARD,
        Queue.FIELD_OPERATIONS,
        ("downed line", "down line", "power line", "tree down", "flood", "debris", "road blocked", "sparks", "sparking", "wire"),
    ),
    (
        SignalCategory.INFRASTRUCTURE_OUTAGE,
        Queue.ENGINEERING,
        ("outage", "no power", "lost power", "power is out", "power's out", "blackout", "transformer", "grid", "substation", "offline", "service down", "system down"),
    ),
    (
        SignalCategory.COMPLIANCE_REPORT,
        Queue.COMPLIANCE_DESK,
        ("recall", "breach", "statutory", "compliance", "regulatory", "deadline", "nfirs", "nibrs", "notification window"),
    ),
    (
        SignalCategory.HUMAN_REQUEST,
        Queue.ESCALATIONS,
        ("speak to a human", "speak to someone", "talk to a person", "real person", "representative", "manager", "agent please"),
    ),
    (
        SignalCategory.STATUS_CHECK,
        Queue.CUSTOMER_COMMS,
        ("status of", "any update", "what's the status", "following up", "follow up", "ticket number"),
    ),
    (
        SignalCategory.CUSTOMER_INQUIRY,
        Queue.CUSTOMER_COMMS,
        ("refund", "bill", "account", "how do i", "when will", "question about", "charge", "invoice"),
    ),
]

_SEVERITY_WORDS = (
    "fire", "smoke", "gas leak", "injured", "trapped", "explosion", "collapse",
    "no power", "outage", "blackout", "sparks", "sparking", "flood", "down",
    "emergency", "danger", "life", "death", "unconscious", "bleeding",
)

_URGENCY_WORDS = ("urgent", "immediately", "now", "asap", "emergency", "right now", "critical")
_FRUSTRATION_WORDS = ("angry", "furious", "frustrated", "ridiculous", "unacceptable", "fed up", "third time")
_HUMAN_WORDS = ("human", "person", "representative", "manager", "agent")


def detect_pii(text: str) -> tuple[bool, list[str]]:
    """Detect PII types present in *text* without echoing the values."""
    types: list[str] = []
    if _SSN_RE.search(text):
        types.append("ssn")
    if _EMAIL_RE.search(text):
        types.append("email")
    if _PHONE_RE.search(text):
        types.append("phone")
    return (len(types) > 0, types)


def classify_signal(text: str) -> SignalClassification:
    """Deterministic keyword classification used by the mock 'model'."""
    lower = text.lower()

    category = SignalCategory.GENERAL_INQUIRY
    queue = Queue.CUSTOMER_COMMS
    matched = False
    for cat, q, words in _CATEGORY_KEYWORDS:
        if any(w in lower for w in words):
            category, queue, matched = cat, q, True
            break

    severity_indicators = [w for w in _SEVERITY_WORDS if w in lower]
    urgency = [w for w in _URGENCY_WORDS if w in lower]

    sentiment = Sentiment.NEUTRAL
    if any(w in lower for w in _FRUSTRATION_WORDS):
        sentiment = Sentiment.FRUSTRATED
    elif urgency:
        sentiment = Sentiment.URGENT

    pii_detected, pii_types = detect_pii(text)

    requires_escalation = False
    escalation_reason: Optional[EscalationReason] = None
    if category is SignalCategory.HUMAN_REQUEST or any(w in lower for w in _HUMAN_WORDS):
        requires_escalation = True
        escalation_reason = EscalationReason.USER_REQUESTED_HUMAN
    elif category is SignalCategory.PUBLIC_SAFETY:
        requires_escalation = True
        escalation_reason = EscalationReason.LIFE_SAFETY
    elif category is SignalCategory.COMPLIANCE_REPORT:
        requires_escalation = True
        escalation_reason = EscalationReason.STATUTORY_CLOCK

    # Confidence: strong when a category matched and we have corroborating signals.
    confidence = 0.55
    if matched:
        confidence = 0.82
        if severity_indicators or urgency:
            confidence = 0.93
        elif category in (SignalCategory.CUSTOMER_INQUIRY, SignalCategory.STATUS_CHECK):
            confidence = 0.88

    location = _extract_location(text)
    system = _extract_system(lower)

    return SignalClassification(
        intent=_intent_for(category),
        intent_category=category,
        target_queue=queue,
        confidence=confidence,
        entities=SignalEntities(
            location=location,
            system=system,
            severity_indicators=severity_indicators,
        ),
        requires_escalation=requires_escalation,
        escalation_reason=escalation_reason,
        pii_detected=pii_detected,
        pii_types=pii_types,
        sentiment=sentiment,
        urgency_indicators=urgency,
    )


def _intent_for(category: SignalCategory) -> str:
    return {
        SignalCategory.PUBLIC_SAFETY: "report_safety_threat",
        SignalCategory.FIELD_HAZARD: "report_field_hazard",
        SignalCategory.INFRASTRUCTURE_OUTAGE: "report_outage",
        SignalCategory.COMPLIANCE_REPORT: "file_compliance_report",
        SignalCategory.HUMAN_REQUEST: "request_human",
        SignalCategory.STATUS_CHECK: "check_status",
        SignalCategory.CUSTOMER_INQUIRY: "customer_inquiry",
        SignalCategory.SERVICE_REQUEST: "service_request",
        SignalCategory.GENERAL_INQUIRY: "general_inquiry",
    }[category]


_LOCATION_RE = re.compile(
    r"\b(?:at|on|near|by)\s+([A-Z0-9][\w]*(?:\s+(?:&|and|st|street|ave|avenue|rd|road|blvd|\d+(?:th|st|nd|rd)?)\.?\s*)*[\w&]*)",
)


def _extract_location(text: str) -> Optional[str]:
    m = _LOCATION_RE.search(text)
    if m:
        loc = m.group(1).strip().rstrip(".")
        return loc or None
    return None


def _extract_system(lower: str) -> Optional[str]:
    for token in ("power grid", "grid", "transformer", "substation", "water main", "network", "app", "website", "phone line"):
        if token in lower:
            return token
    return None


class MockChatClient(BaseChatClient):
    """Offline twin of a chat client (plan.md Appendix B contract)."""

    async def _inner_get_response(  # type: ignore[override]
        self,
        *,
        messages: Sequence[Message],
        stream: bool = False,
        options: Mapping[str, Any] | None = None,
        **kwargs: Any,
    ) -> ChatResponse:
        response_format = self._response_format(options)
        user_text = self._latest_user_text(messages)

        if response_format is SignalClassification:
            value = classify_signal(user_text)
            return ChatResponse(
                messages=[Message("assistant", value.model_dump_json())],
                value=value,
                response_format=response_format,
            )

        if response_format is not None and isinstance(response_format, type) and issubclass(response_format, BaseModel):
            # Best-effort conformant instance for any other structured model.
            value = response_format.model_construct()
            return ChatResponse(
                messages=[Message("assistant", "{}")],
                value=value,
                response_format=response_format,
            )

        return ChatResponse(messages=[Message("assistant", "All Clear mock acknowledgement.")])

    @staticmethod
    def _response_format(options: Mapping[str, Any] | None) -> Any:
        if options is None:
            return None
        if isinstance(options, Mapping):
            return options.get("response_format")
        return getattr(options, "response_format", None)

    @staticmethod
    def _latest_user_text(messages: Sequence[Message]) -> str:
        for msg in reversed(list(messages)):
            role = getattr(msg, "role", None)
            role_str = getattr(role, "value", role)
            if role_str in ("user", "User", None):
                text = getattr(msg, "text", None)
                if text:
                    return str(text)
        # Fallback: concatenate any text we can find.
        for msg in reversed(list(messages)):
            text = getattr(msg, "text", None)
            if text:
                return str(text)
        return ""
