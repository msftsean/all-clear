"""
RouterExecutor scaffold for the Lab 05 All Clear mini-app.

RouterExecutor is deterministic workflow code. It makes zero LLM calls and owns
dedup, severity/SLA mapping, and escalation. It does not mutate records.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

from query_agent import SignalCategory, SignalClassification


class Severity(str, Enum):
    """All Clear severity/SLA scale."""

    SEV1 = "SEV1"
    SEV2 = "SEV2"
    SEV3 = "SEV3"
    SEV4 = "SEV4"


class RoutingOutcome(str, Enum):
    """Dedup outcome for a signal."""

    ATTACH_TO_INCIDENT = "ATTACH_TO_INCIDENT"
    OPEN_INCIDENT = "OPEN_INCIDENT"


@dataclass
class OpenIncident:
    """Read-only incident summary used for dedup in the lab."""

    incident_id: str
    category: SignalCategory
    summary: str
    magnitude: int = 1


@dataclass(frozen=True)
class RoutingDecision:
    """RouterExecutor output. Deterministic; zero LLM calls."""

    outcome: RoutingOutcome
    target_queue: str
    severity: Severity
    sla_minutes: int
    escalate: bool = False
    escalation_reason: Optional[str] = None
    matched_incident_id: Optional[str] = None
    dedup_similarity: Optional[float] = None
    magnitude: Optional[int] = None
    routing_rules_applied: list[str] = field(default_factory=list)
    classification: Optional[SignalClassification] = None
    signal_text: str = ""


DEDUP_THRESHOLD = 0.83
SLA_MINUTES = {Severity.SEV1: 15, Severity.SEV2: 60, Severity.SEV3: 240, Severity.SEV4: 1440}
QUEUE_FOR = {
    SignalCategory.INFRASTRUCTURE_OUTAGE: "engineering",
    SignalCategory.FIELD_HAZARD: "field-operations",
    SignalCategory.PUBLIC_SAFETY: "field-operations",
    SignalCategory.CUSTOMER_INQUIRY: "customer-comms",
    SignalCategory.SERVICE_REQUEST: "customer-comms",
    SignalCategory.COMPLIANCE_REPORT: "compliance-desk",
    SignalCategory.STATUS_CHECK: "customer-comms",
    SignalCategory.HUMAN_REQUEST: "escalations",
    SignalCategory.GENERAL_INQUIRY: "customer-comms",
}


class RouterExecutor:
    """Deterministic routing executor: dedup -> severity -> SLA -> escalation."""

    def __init__(self, open_incidents: list[OpenIncident] | None = None) -> None:
        self.open_incidents = open_incidents or []

    async def route(self, classification: SignalClassification, signal_text: str | None = None) -> RoutingDecision:
        """Route a classified signal without calling an LLM."""
        text = signal_text or classification.signal_text
        rules: list[str] = []
        severity = self._severity(classification)
        # TODO: Keep this deterministic; do not add model calls here.
        rules.append(f"severity={severity.value}")
        sla_minutes = SLA_MINUTES[severity]

        matched, similarity = self._best_match(text, classification.category)
        if classification.category == SignalCategory.STATUS_CHECK and not matched:
            rules.append("status_check_no_new_incident")
            return RoutingDecision(
                outcome=RoutingOutcome.ATTACH_TO_INCIDENT,
                target_queue=QUEUE_FOR[classification.category],
                severity=Severity.SEV4,
                sla_minutes=SLA_MINUTES[Severity.SEV4],
                dedup_similarity=similarity,
                routing_rules_applied=rules,
                classification=classification,
                signal_text=text,
            )

        if matched and similarity >= DEDUP_THRESHOLD:
            rules.append(f"dedup>={DEDUP_THRESHOLD}")
            return RoutingDecision(
                outcome=RoutingOutcome.ATTACH_TO_INCIDENT,
                target_queue=QUEUE_FOR[classification.category],
                severity=severity,
                sla_minutes=sla_minutes,
                matched_incident_id=matched.incident_id,
                dedup_similarity=similarity,
                magnitude=matched.magnitude + 1,
                routing_rules_applied=rules,
                classification=classification,
                signal_text=text,
            )

        escalate, reason = self._escalation(classification, severity)
        if escalate:
            rules.append(f"escalate:{reason}")

        return RoutingDecision(
            outcome=RoutingOutcome.OPEN_INCIDENT,
            target_queue=QUEUE_FOR[classification.category],
            severity=severity,
            sla_minutes=sla_minutes,
            escalate=escalate,
            escalation_reason=reason,
            dedup_similarity=similarity,
            routing_rules_applied=rules,
            classification=classification,
            signal_text=text,
        )

    def _severity(self, classification: SignalClassification) -> Severity:
        haystack = " ".join(classification.severity_indicators_all() + [classification.signal_text]).lower()
        if classification.category in {SignalCategory.PUBLIC_SAFETY, SignalCategory.COMPLIANCE_REPORT}:
            return Severity.SEV1
        if any(word in haystack for word in ("fire", "gas", "injured", "trapped", "school", "statutory", "no power")):
            return Severity.SEV1
        if classification.category in {SignalCategory.INFRASTRUCTURE_OUTAGE, SignalCategory.FIELD_HAZARD}:
            return Severity.SEV2
        if classification.category in {SignalCategory.CUSTOMER_INQUIRY, SignalCategory.SERVICE_REQUEST, SignalCategory.STATUS_CHECK, SignalCategory.GENERAL_INQUIRY}:
            return Severity.SEV4
        return Severity.SEV3

    def _escalation(self, classification: SignalClassification, severity: Severity) -> tuple[bool, Optional[str]]:
        if severity == Severity.SEV1:
            return True, "sev1_incident"
        if classification.category == SignalCategory.HUMAN_REQUEST:
            return True, "user_requested_human"
        if classification.pii_detected:
            return True, "pii_exposure"
        if classification.confidence < 0.70:
            return True, "confidence_too_low"
        return False, None

    def _best_match(self, signal_text: str, category: SignalCategory) -> tuple[Optional[OpenIncident], Optional[float]]:
        candidates = [incident for incident in self.open_incidents if incident.category == category]
        if not candidates:
            return None, None
        scored = [(incident, self._token_similarity(signal_text, incident.summary)) for incident in candidates]
        return max(scored, key=lambda item: item[1])

    def _token_similarity(self, left: str, right: str) -> float:
        left_tokens = set(left.lower().split())
        right_tokens = set(right.lower().split())
        if not left_tokens or not right_tokens:
            return 0.0
        overlap = len(left_tokens & right_tokens)
        return overlap / math.sqrt(len(left_tokens) * len(right_tokens))

    def add_open_incident(self, incident: OpenIncident) -> None:
        """Lab helper for building a dedup fixture."""
        self.open_incidents.append(incident)

