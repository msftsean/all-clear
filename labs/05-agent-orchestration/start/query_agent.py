"""
QueryAgent scaffold for the Lab 05 All Clear mini-app.

QueryAgent classifies one inbound signal. It does not route, deduplicate,
open incidents, search knowledge, assign severity, or generate a sitrep.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional


class SignalCategory(str, Enum):
    """All Clear signal category taxonomy."""

    INFRASTRUCTURE_OUTAGE = "INFRASTRUCTURE_OUTAGE"
    FIELD_HAZARD = "FIELD_HAZARD"
    PUBLIC_SAFETY = "PUBLIC_SAFETY"
    CUSTOMER_INQUIRY = "CUSTOMER_INQUIRY"
    SERVICE_REQUEST = "SERVICE_REQUEST"
    COMPLIANCE_REPORT = "COMPLIANCE_REPORT"
    STATUS_CHECK = "STATUS_CHECK"
    HUMAN_REQUEST = "HUMAN_REQUEST"
    GENERAL_INQUIRY = "GENERAL_INQUIRY"


@dataclass(frozen=True)
class SignalEntities:
    """Entities extracted from one signal."""

    location: Optional[str] = None
    system: Optional[str] = None
    severity_indicators: list[str] = field(default_factory=list)
    other: list[str] = field(default_factory=list)

    def as_dict(self) -> dict[str, Any]:
        return {
            "location": self.location,
            "system": self.system,
            "severity_indicators": list(self.severity_indicators),
            "other": list(self.other),
        }


@dataclass(frozen=True)
class SignalClassification:
    """QueryAgent output. Authority: classify only."""

    signal_text: str
    category: SignalCategory
    confidence: float
    entities: SignalEntities = field(default_factory=SignalEntities)
    pii_detected: bool = False
    pii_types: list[str] = field(default_factory=list)
    urgency_indicators: list[str] = field(default_factory=list)
    requires_clarification: bool = False
    clarification_question: Optional[str] = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def severity_indicators_all(self) -> list[str]:
        return list(self.entities.severity_indicators) + list(self.urgency_indicators)


CATEGORY_KEYWORDS: dict[SignalCategory, tuple[str, ...]] = {
    SignalCategory.PUBLIC_SAFETY: ("gas", "fire", "smoke", "explosion", "injured", "trapped", "school", "sparking", "power line"),
    SignalCategory.FIELD_HAZARD: ("power line", "downed line", "sparking", "water main", "flood", "blocked road", "tree down"),
    SignalCategory.INFRASTRUCTURE_OUTAGE: ("outage", "no power", "blackout", "transformer", "substation", "grid", "offline"),
    SignalCategory.COMPLIANCE_REPORT: ("nfirs", "nibrs", "recall", "breach notification", "statutory", "compliance"),
    SignalCategory.STATUS_CHECK: ("any update", "status", "crew eta", "already reported", "ac-"),
    SignalCategory.HUMAN_REQUEST: ("human", "real person", "supervisor", "manager", "representative", "escalate"),
    SignalCategory.CUSTOMER_INQUIRY: ("when will", "how long", "eta", "restored", "is it safe"),
    SignalCategory.SERVICE_REQUEST: ("schedule", "inspection", "appointment", "meter", "service request", "routine"),
}
CATEGORY_PRECEDENCE = [SignalCategory.COMPLIANCE_REPORT, SignalCategory.PUBLIC_SAFETY, SignalCategory.STATUS_CHECK, SignalCategory.FIELD_HAZARD, SignalCategory.INFRASTRUCTURE_OUTAGE, SignalCategory.HUMAN_REQUEST, SignalCategory.CUSTOMER_INQUIRY, SignalCategory.SERVICE_REQUEST]
AC_ID_RE = re.compile(r"\bAC-\d{4,}\b", re.IGNORECASE)
PHONE_RE = re.compile(r"\b(?:\+?1[-. ]?)?\(?\d{3}\)?[-. ]?\d{3}[-. ]?\d{4}\b")
EMAIL_RE = re.compile(r"\b[\w.+-]+@[\w.-]+\.\w+\b")


class QueryAgent:
    """Classifies inbound All Clear signals into structured categories."""

    SYSTEM_PROMPT = """You are the QueryAgent for All Clear. Classify one inbound signal into a SignalCategory and extract location, system, severity_indicators, PII flags, and confidence. You classify only; never route, deduplicate, open incidents, search knowledge, assign severity, or generate a sitrep. Return JSON only."""

    def __init__(self, client: Any = None, model: str = "gpt-5.1") -> None:
        self.client = client
        self.model = model

    async def classify(self, signal_text: str, conversation_context: str | None = None) -> SignalClassification:
        """Classify one inbound signal. Falls back to deterministic rules without Azure."""
        if not signal_text or not signal_text.strip():
            raise ValueError("Signal cannot be empty")
        if self.client is None:
            # TODO: Replace the deterministic helper with your QueryAgent prompt when Azure is configured.
            return self._classify_with_rules(signal_text)

        prompt = self._build_classification_prompt(signal_text, conversation_context)
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "system", "content": self.SYSTEM_PROMPT}, {"role": "user", "content": prompt}],
            temperature=0.1,
            response_format={"type": "json_object"},
        )
        data = json.loads(response.choices[0].message.content)
        return self._from_json(signal_text, data)

    async def analyze(self, signal_text: str, conversation_context: str | None = None) -> SignalClassification:
        """Backward-compatible wrapper for older lab harnesses."""
        return await self.classify(signal_text, conversation_context)

    def _build_classification_prompt(self, signal_text: str, conversation_context: str | None = None) -> str:
        parts = []
        if conversation_context:
            parts.append(f"Session context:\n{conversation_context}")
        parts.append(f"Current signal:\n{signal_text}")
        parts.append("Classify this signal and respond with JSON.")
        return "\n\n".join(parts)

    def _from_json(self, signal_text: str, data: dict[str, Any]) -> SignalClassification:
        category_value = data.get("category", data.get("signal_category", "GENERAL_INQUIRY"))
        category = SignalCategory(category_value) if category_value in SignalCategory._value2member_map_ else SignalCategory.GENERAL_INQUIRY
        entities_data = data.get("entities", {}) or {}
        return SignalClassification(
            signal_text=signal_text,
            category=category,
            confidence=float(data.get("confidence", 0.5)),
            entities=SignalEntities(
                location=entities_data.get("location"),
                system=entities_data.get("system"),
                severity_indicators=list(entities_data.get("severity_indicators", [])),
                other=list(entities_data.get("other", [])),
            ),
            pii_detected=bool(data.get("pii_detected", False)),
            pii_types=list(data.get("pii_types", [])),
            urgency_indicators=list(data.get("urgency_indicators", [])),
            requires_clarification=bool(data.get("requires_clarification", False)),
            clarification_question=data.get("clarification_question"),
        )

    def _classify_with_rules(self, signal_text: str) -> SignalClassification:
        text = signal_text.lower()
        scores: dict[SignalCategory, int] = {}
        indicators: list[str] = []
        for category, keywords in CATEGORY_KEYWORDS.items():
            hits = [kw for kw in keywords if kw in text]
            if hits:
                scores[category] = len(hits)
                indicators.extend(hits)
        if AC_ID_RE.search(signal_text):
            scores[SignalCategory.STATUS_CHECK] = scores.get(SignalCategory.STATUS_CHECK, 0) + 2
        category = self._best_category(scores) if scores else SignalCategory.GENERAL_INQUIRY
        confidence = 0.55 if not scores else min(0.98, 0.70 + max(scores.values()) * 0.08)
        pii_types = []
        if PHONE_RE.search(signal_text):
            pii_types.append("phone")
        if EMAIL_RE.search(signal_text):
            pii_types.append("email")
        return SignalClassification(
            signal_text=signal_text,
            category=category,
            confidence=confidence,
            entities=SignalEntities(
                location=self._extract_location(signal_text),
                system=self._extract_system(text),
                severity_indicators=sorted(set(indicators)),
                other=AC_ID_RE.findall(signal_text),
            ),
            pii_detected=bool(pii_types),
            pii_types=pii_types,
            urgency_indicators=[kw for kw in ("urgent", "immediately", "statutory", "now") if kw in text],
            requires_clarification=confidence < 0.60,
            clarification_question="Can you share the location and what is happening?" if confidence < 0.60 else None,
        )

    def _best_category(self, scores: dict[SignalCategory, int]) -> SignalCategory:
        best_score = max(scores.values())
        tied = {category for category, score in scores.items() if score == best_score}
        for category in CATEGORY_PRECEDENCE:
            if category in tied:
                return category
        return SignalCategory.GENERAL_INQUIRY

    def _extract_location(self, signal_text: str) -> Optional[str]:
        match = re.search(r"(?:at|near|on|across)\s+([^,.!?]+)", signal_text, re.IGNORECASE)
        return match.group(1).strip() if match else None

    def _extract_system(self, text: str) -> Optional[str]:
        for system in ("power line", "water main", "transformer", "substation", "grid", "gas"):
            if system in text:
                return system
        return None

