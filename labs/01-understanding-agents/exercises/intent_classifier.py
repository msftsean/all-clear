"""
Signal Classification Exercise - Lab 01a.

This lightweight classifier models the All Clear QueryAgent: it maps one inbound
signal to an All Clear SignalCategory. QueryAgent classifies only; RouterExecutor
later handles dedup, SEV1-SEV4, SLA, and escalation.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from enum import Enum
from typing import Literal

SignalCategoryName = Literal[
    "INFRASTRUCTURE_OUTAGE", "FIELD_HAZARD", "PUBLIC_SAFETY",
    "CUSTOMER_INQUIRY", "SERVICE_REQUEST", "COMPLIANCE_REPORT",
    "STATUS_CHECK", "HUMAN_REQUEST", "GENERAL_INQUIRY", "unknown",
]


class SignalCategory(str, Enum):
    """All Clear SignalCategory taxonomy."""

    INFRASTRUCTURE_OUTAGE = "INFRASTRUCTURE_OUTAGE"
    FIELD_HAZARD = "FIELD_HAZARD"
    PUBLIC_SAFETY = "PUBLIC_SAFETY"
    CUSTOMER_INQUIRY = "CUSTOMER_INQUIRY"
    SERVICE_REQUEST = "SERVICE_REQUEST"
    COMPLIANCE_REPORT = "COMPLIANCE_REPORT"
    STATUS_CHECK = "STATUS_CHECK"
    HUMAN_REQUEST = "HUMAN_REQUEST"
    GENERAL_INQUIRY = "GENERAL_INQUIRY"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class ClassificationResult:
    """Small exercise result with a category and confidence score."""

    intent: SignalCategory
    confidence: float
    matched_keywords: tuple[str, ...] = ()


CATEGORY_KEYWORDS: dict[SignalCategory, dict[str, float]] = {
    SignalCategory.PUBLIC_SAFETY: {
        "smell of gas": 4, "gas leak": 4, "fire": 3.5, "smoke": 3,
        "explosion": 4, "injured": 4, "trapped": 4, "unconscious": 4,
        "life safety": 4, "near a school": 2.5,
    },
    SignalCategory.FIELD_HAZARD: {
        "power line down": 4, "downed line": 4, "line down": 3.5,
        "sparking": 3.5, "wire down": 3.5, "water main break": 4,
        "flooding": 3.5, "flood": 2.5, "blocked road": 3,
        "blocked street": 3, "tree down": 3, "debris": 2, "hazard": 2,
    },
    SignalCategory.INFRASTRUCTURE_OUTAGE: {
        "outage": 3, "no power": 3.5, "lost power": 3.5, "blackout": 3.5,
        "transformer": 2.5, "substation": 3, "grid": 2.5,
        "service is down": 3, "systems offline": 3, "whole neighborhood": 2.5,
        "surge": 1.5,
    },
    SignalCategory.COMPLIANCE_REPORT: {
        "nfirs": 4, "nibrs": 4, "recall": 3.5, "product recall": 4,
        "breach notification": 4, "statutory": 4, "regulatory": 3,
        "compliance": 3, "reporting deadline": 3.5, "must be filed": 3,
        "file the report": 3,
    },
    SignalCategory.STATUS_CHECK: {
        "incident status": 3.5, "status of incident": 3.5, "any update": 3,
        "already reported": 3, "crew eta": 3, "update on": 2.5,
        "follow up": 2.5, "ac-": 4,
    },
    SignalCategory.HUMAN_REQUEST: {
        "real person": 4, "representative": 3.5, "supervisor": 3.5,
        "manager": 3, "human": 3, "escalate": 3, "someone in charge": 3.5,
        "talk to someone": 3,
    },
    SignalCategory.CUSTOMER_INQUIRY: {
        "when will": 3.5, "eta": 3, "estimated time": 3,
        "power restored": 3, "restored": 2, "how long": 2.5,
        "what is the status": 2.5, "can you tell me": 2, "is it safe": 2,
        "information": 1.5,
    },
    SignalCategory.SERVICE_REQUEST: {
        "schedule": 3, "appointment": 3, "inspection": 3, "meter": 2.5,
        "service request": 3.5, "turn on service": 3, "routine": 2.5,
        "non-urgent": 2.5, "pickup": 2,
    },
}

CATEGORY_PRECEDENCE = [
    SignalCategory.PUBLIC_SAFETY, SignalCategory.FIELD_HAZARD,
    SignalCategory.INFRASTRUCTURE_OUTAGE, SignalCategory.COMPLIANCE_REPORT,
    SignalCategory.STATUS_CHECK, SignalCategory.HUMAN_REQUEST,
    SignalCategory.CUSTOMER_INQUIRY, SignalCategory.SERVICE_REQUEST,
]
GREETING_OR_THANKS = re.compile(r"^(hello|hi|hey|good morning|good afternoon|good evening|thanks|thank you)\b", re.I)
AC_ID_PATTERN = re.compile(r"\bAC-\d{3,}\b", re.I)


def _normalize(signal: object) -> str:
    if signal is None:
        return ""
    return str(signal).lower().strip()


def _score_signal(signal_lower: str) -> dict[SignalCategory, tuple[float, list[str]]]:
    scores: dict[SignalCategory, tuple[float, list[str]]] = {}
    for category, keywords in CATEGORY_KEYWORDS.items():
        score = 0.0
        matches: list[str] = []
        for keyword, weight in keywords.items():
            if keyword in signal_lower:
                score += weight
                matches.append(keyword)
        if category is SignalCategory.STATUS_CHECK and AC_ID_PATTERN.search(signal_lower):
            score += 4
            matches.append("AC-####")
        if score > 0:
            scores[category] = (score, matches)
    return scores


def _best_category(scores: dict[SignalCategory, tuple[float, list[str]]]) -> SignalCategory:
    best_score = max(score for score, _ in scores.values())
    tied = {category for category, (score, _) in scores.items() if score == best_score}
    for category in CATEGORY_PRECEDENCE:
        if category in tied:
            return category
    return SignalCategory.GENERAL_INQUIRY


def classify_intent(signal: object) -> SignalCategoryName:
    """Classify one inbound All Clear signal into a SignalCategory value."""
    signal_lower = _normalize(signal)
    if not signal_lower or len(signal_lower) < 2 or re.fullmatch(r"[\W_\d]+", signal_lower):
        return "unknown"

    scores = _score_signal(signal_lower)
    if scores:
        return _best_category(scores).value  # type: ignore[return-value]
    if GREETING_OR_THANKS.search(signal_lower) or len(signal_lower.split()) >= 3:
        return SignalCategory.GENERAL_INQUIRY.value
    return "unknown"


class IntentClassifier:
    """Compatibility wrapper used by lab verification scripts."""

    def classify(self, signal: object) -> ClassificationResult:
        category = SignalCategory(classify_intent(signal))
        scores = _score_signal(_normalize(signal))
        score, matched = scores.get(category, (0.0, []))
        if category is SignalCategory.UNKNOWN:
            confidence = 0.0
        elif category is SignalCategory.GENERAL_INQUIRY and not matched:
            confidence = 0.55
        else:
            confidence = min(0.99, 0.55 + score * 0.1)
        return ClassificationResult(category, round(confidence, 2), tuple(matched))


if __name__ == "__main__":
    test_signals = [
        "Power line down across Main St, sparking near a school",
        "Water main break flooding the 200 block",
        "When will power be restored on Elm St?",
        "Smell of gas near the community center",
        "Need to file the NFIRS report for last night's fire",
        "Any update on AC-0042?",
    ]
    print("Testing All Clear Signal Classifier\n")
    for item in test_signals:
        result = IntentClassifier().classify(item)
        print(f"Signal: {item}")
        print(f"Category: {result.intent.value} (confidence={result.confidence})\n")

