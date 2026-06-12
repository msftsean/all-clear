"""
RouterExecutor: deterministic dedup, severity/SLA mapping, and escalation (001-maf-rehost, T7).

Bounded Authority (Constitution Art. II):
- CAN: deduplicate an inbound signal against open incidents (read-only), map severity
  from classification indicators by RULES, compute the SLA clock, and decide escalation.
- CANNOT: classify (QueryAgent's job), persist or mutate incidents (ActionAgent's job),
  or call any language model. This module imports NO model/LLM client by design and
  by test (tests/test_router_no_llm.py + Constitution Art. II).

This is a plain MAF ``Executor`` (Appendix B), NOT an LLM agent. Every decision here is
a pure function of the SignalClassification plus the open-incident vectors it reads from
the injected IncidentStore. All thresholds (dedup cosine, per-severity SLA minutes,
confidence floor) come from Settings, never hard-coded magic numbers.
"""

from __future__ import annotations

import math
from typing import Optional

from agent_framework import Executor, WorkflowContext, handler

from app.agents.envelopes import ClassifiedSignal, RoutedSignal
from app.agents.schemas import (
    EscalationReason,
    Queue,
    RoutingDecision,
    RoutingOutcome,
    Severity,
    SignalCategory,
    SignalClassification,
)
from app.core.config import Settings
from app.services.interfaces import EmbeddingFn, IncidentStoreInterface

# Category -> destination queue. Routing is by rule, never by model vibes (CONTEXT.md).
CATEGORY_TO_QUEUE: dict[SignalCategory, Queue] = {
    SignalCategory.INFRASTRUCTURE_OUTAGE: Queue.ENGINEERING,
    SignalCategory.FIELD_HAZARD: Queue.FIELD_OPERATIONS,
    SignalCategory.PUBLIC_SAFETY: Queue.FIELD_OPERATIONS,
    SignalCategory.CUSTOMER_INQUIRY: Queue.CUSTOMER_COMMS,
    SignalCategory.SERVICE_REQUEST: Queue.CUSTOMER_COMMS,
    SignalCategory.COMPLIANCE_REPORT: Queue.COMPLIANCE_DESK,
    SignalCategory.STATUS_CHECK: Queue.CUSTOMER_COMMS,
    SignalCategory.HUMAN_REQUEST: Queue.ESCALATIONS,
    SignalCategory.GENERAL_INQUIRY: Queue.CUSTOMER_COMMS,
}

# Phrases that force SEV1 (life safety). Matched against entity severity indicators.
_LIFE_SAFETY_TERMS = (
    "fire", "smoke", "gas leak", "injured", "trapped", "explosion",
    "collapse", "unconscious", "bleeding", "death", "danger", "life",
)

# PII types that warrant a human handoff (Constitution Art. I: protect sensitive data).
_SENSITIVE_PII = ("ssn", "credit_card")


def _cosine(a: list[float], b: list[float]) -> float:
    """Cosine similarity of two equal-length vectors (0.0 if either is degenerate)."""
    if not a or not b or len(a) != len(b):
        return 0.0
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    if na == 0.0 or nb == 0.0:
        return 0.0
    return dot / (na * nb)


class RouterExecutor(Executor):
    """Deterministic routing stage. Produces a RoutingDecision; mutates nothing."""

    def __init__(
        self,
        embed: EmbeddingFn,
        store: IncidentStoreInterface,
        settings: Settings,
        *,
        id: str = "router",
    ) -> None:
        super().__init__(id=id)
        self._embed = embed
        self._store = store
        self._settings = settings

    @handler
    async def route(
        self, message: ClassifiedSignal, ctx: WorkflowContext[RoutedSignal]
    ) -> None:
        decision, embedding = await self.decide(message.signal_text, message.classification)
        await ctx.send_message(
            RoutedSignal(
                signal_text=message.signal_text,
                classification=message.classification,
                routing=decision,
                embedding=embedding,
                session_id=message.session_id,
                channel=message.channel,
            )
        )

    async def decide(
        self, signal_text: str, classification: SignalClassification
    ) -> tuple[RoutingDecision, list[float]]:
        """Pure routing decision for one classified signal.

        Returns the RoutingDecision and the signal embedding (carried forward so the
        OPEN_INCIDENT path can persist it without recomputation).
        """
        rules: list[str] = []
        embedding = await self._embed(signal_text)

        # --- Step 1: dedup against open incidents in the SAME category (read-only) ---
        category = classification.intent_category
        vectors = await self._store.get_open_incident_vectors(category)
        best_id: Optional[str] = None
        best_sim = 0.0
        for incident_id, vector in vectors:
            sim = _cosine(embedding, vector)
            if sim > best_sim:
                best_sim, best_id = sim, incident_id

        if best_id is not None and best_sim >= self._settings.dedup_threshold:
            rules.append(f"dedup_match>={self._settings.dedup_threshold}")
            return (await self._attach_decision(best_id, best_sim, rules), embedding)

        rules.append("dedup_no_match")

        # --- Step 2: severity/SLA mapping by rule (never model vibes) ---
        severity = self._map_severity(classification, rules)
        sla_minutes = self._sla_for(severity)
        queue = CATEGORY_TO_QUEUE.get(category, Queue.CUSTOMER_COMMS)
        rules.append(f"queue_{queue.value}")
        rules.append(f"severity_{severity.value}")

        # --- Step 3: escalation rules ---
        escalate, reason = self._check_escalation(classification, severity, rules)

        decision = RoutingDecision(
            outcome=RoutingOutcome.OPEN_INCIDENT,
            target_queue=queue,
            severity=severity,
            sla_minutes=sla_minutes,
            escalate=escalate,
            escalation_reason=reason,
            matched_incident_id=None,
            dedup_similarity=round(best_sim, 4) if vectors else None,
            magnitude=1,
            routing_rules_applied=rules,
        )
        return (decision, embedding)

    async def _attach_decision(
        self, incident_id: str, similarity: float, rules: list[str]
    ) -> RoutingDecision:
        """Build an ATTACH_TO_INCIDENT decision from the matched incident (read-only).

        The actual report attachment / magnitude increment is performed downstream by
        ActionAgent; the RouterExecutor only reads the incident to mirror its severity,
        SLA, and queue so the decision is internally consistent.
        """
        incident = await self._store.get_incident(incident_id)
        if incident is None:  # pragma: no cover - defensive; vector implies incident
            raise ValueError(f"dedup matched missing incident {incident_id}")
        rules.append("attach_short_ack_no_knowledge_search")
        return RoutingDecision(
            outcome=RoutingOutcome.ATTACH_TO_INCIDENT,
            target_queue=incident.queue,
            severity=incident.severity,
            sla_minutes=incident.sla_minutes,
            escalate=incident.escalated,
            escalation_reason=EscalationReason.SEV1_INCIDENT if incident.escalated else None,
            matched_incident_id=incident_id,
            dedup_similarity=round(similarity, 4),
            magnitude=incident.magnitude + 1,
            routing_rules_applied=rules,
        )

    def _map_severity(
        self, classification: SignalClassification, rules: list[str]
    ) -> Severity:
        category = classification.intent_category
        indicators = {i.lower() for i in classification.entities.severity_indicators}
        statutory = (
            category is SignalCategory.COMPLIANCE_REPORT
            or classification.escalation_reason is EscalationReason.STATUTORY_CLOCK
        )
        life_safety = category is SignalCategory.PUBLIC_SAFETY or any(
            term in indicator for term in _LIFE_SAFETY_TERMS for indicator in indicators
        )

        if statutory:
            rules.append("sev1_statutory_clock")
            return Severity.SEV1
        if life_safety:
            rules.append("sev1_life_safety")
            return Severity.SEV1
        if category in (SignalCategory.INFRASTRUCTURE_OUTAGE, SignalCategory.FIELD_HAZARD):
            return Severity.SEV2
        if category in (SignalCategory.CUSTOMER_INQUIRY, SignalCategory.HUMAN_REQUEST):
            return Severity.SEV3
        return Severity.SEV4

    def _sla_for(self, severity: Severity) -> int:
        return {
            Severity.SEV1: self._settings.sla_sev1_minutes,
            Severity.SEV2: self._settings.sla_sev2_minutes,
            Severity.SEV3: self._settings.sla_sev3_minutes,
            Severity.SEV4: self._settings.sla_sev4_minutes,
        }[severity]

    def _check_escalation(
        self,
        classification: SignalClassification,
        severity: Severity,
        rules: list[str],
    ) -> tuple[bool, Optional[EscalationReason]]:
        category = classification.intent_category
        if severity is Severity.SEV1:
            if category is SignalCategory.COMPLIANCE_REPORT or (
                classification.escalation_reason is EscalationReason.STATUTORY_CLOCK
            ):
                reason = EscalationReason.STATUTORY_CLOCK
            elif category is SignalCategory.PUBLIC_SAFETY:
                reason = EscalationReason.LIFE_SAFETY
            else:
                reason = EscalationReason.SEV1_INCIDENT
            rules.append(f"escalate_{reason.value}")
            return (True, reason)

        if category is SignalCategory.HUMAN_REQUEST or (
            classification.requires_escalation
            and classification.escalation_reason is EscalationReason.USER_REQUESTED_HUMAN
        ):
            rules.append("escalate_user_requested_human")
            return (True, EscalationReason.USER_REQUESTED_HUMAN)

        if any(p in _SENSITIVE_PII for p in classification.pii_types):
            rules.append("escalate_pii_exposure")
            return (True, EscalationReason.PII_EXPOSURE)

        if classification.confidence < self._settings.confidence_threshold:
            rules.append("escalate_confidence_too_low")
            return (True, EscalationReason.CONFIDENCE_TOO_LOW)

        return (False, None)
