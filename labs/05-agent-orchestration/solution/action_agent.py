"""
ActionAgent for the Lab 05 All Clear mini-app.

ActionAgent acts through exactly three tools: create_incident, search_knowledge,
and generate_sitrep. Sitreps are citation-grounded: no citation, no claim.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Optional

from router_agent import RoutingDecision, RoutingOutcome, Severity


@dataclass(frozen=True)
class Citation:
    """Source record backing a factual claim."""

    source_id: str
    source_type: str
    quote: str


@dataclass(frozen=True)
class KnowledgeArticle:
    """Knowledge record returned by search_knowledge."""

    article_id: str
    title: str
    snippet: str
    relevance_score: float


@dataclass(frozen=True)
class SitrepDraft:
    """Citation-grounded situation report."""

    incident_id: str
    summary: str
    citations: list[Citation] = field(default_factory=list)


@dataclass(frozen=True)
class IncidentAction:
    """ActionAgent output."""

    status: str
    incident_id: Optional[str]
    queue: str
    severity: Severity
    citations: list[Citation] = field(default_factory=list)
    estimated_response_time: str = "next business day"
    escalated: bool = False
    user_message: str = ""
    sitrep: Optional[SitrepDraft] = None
    knowledge_articles: list[KnowledgeArticle] = field(default_factory=list)
    confidence: float = 0.9
    requires_followup: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def content(self) -> str:
        """Compatibility alias for older lab harnesses."""
        return self.user_message

    @property
    def sources(self) -> list[dict[str, str]]:
        """Compatibility alias for citation display."""
        return [{"id": c.source_id, "type": c.source_type, "quote": c.quote} for c in self.citations]


class ActionAgent:
    """Executes RoutingDecision outcomes through three explicit tools."""

    def __init__(self) -> None:
        self._next_incident_number = 1
        self.incidents: dict[str, dict[str, Any]] = {}

    async def execute(self, decision: RoutingDecision, conversation_history: Optional[list[dict]] = None) -> IncidentAction:
        """Run the correct action path for a routing decision."""
        if decision.outcome == RoutingOutcome.ATTACH_TO_INCIDENT:
            incident_id = decision.matched_incident_id
            magnitude = decision.magnitude or 1
            if incident_id is None:
                return IncidentAction(
                    status="attached",
                    incident_id=None,
                    queue=decision.target_queue,
                    severity=decision.severity,
                    estimated_response_time=self._sla_text(decision.sla_minutes),
                    escalated=decision.escalate,
                    user_message="No new incident was opened for this status check; customer-comms will follow up with available incident information.",
                    metadata={"outcome": decision.outcome.value},
                )
            return IncidentAction(
                status="attached",
                incident_id=incident_id,
                queue=decision.target_queue,
                severity=decision.severity,
                estimated_response_time=self._sla_text(decision.sla_minutes),
                escalated=decision.escalate,
                user_message=f"Thanks — this signal was attached as a report to {incident_id}. Magnitude is now {magnitude}.",
                metadata={"outcome": decision.outcome.value, "magnitude": magnitude},
            )

        incident = self.create_incident(decision)
        articles = self.search_knowledge(decision)
        sitrep = self.generate_sitrep(incident, decision, articles)
        citations = list(sitrep.citations)
        escalation_text = " It has been escalated." if decision.escalate else ""
        return IncidentAction(
            status="opened",
            incident_id=incident["incident_id"],
            queue=decision.target_queue,
            severity=decision.severity,
            citations=citations,
            estimated_response_time=self._sla_text(decision.sla_minutes),
            escalated=decision.escalate,
            user_message=(
                f"Opened incident {incident['incident_id']} in {decision.target_queue} "
                f"at {decision.severity.value} with a {self._sla_text(decision.sla_minutes)} response SLA."
                f"{escalation_text}"
            ),
            sitrep=sitrep,
            knowledge_articles=articles,
            metadata={"outcome": decision.outcome.value, "rules": decision.routing_rules_applied},
        )

    # Tool 1 of 3
    def create_incident(self, decision: RoutingDecision) -> dict[str, Any]:
        """Open a new AC-#### incident from an OPEN_INCIDENT decision."""
        incident_id = f"AC-{self._next_incident_number:04d}"
        self._next_incident_number += 1
        incident = {
            "incident_id": incident_id,
            "queue": decision.target_queue,
            "severity": decision.severity.value,
            "summary": decision.signal_text,
            "category": decision.classification.category.value if decision.classification else "GENERAL_INQUIRY",
            "magnitude": 1,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "escalated": decision.escalate,
        }
        if not re.match(r"^AC-\d{4,}$", incident_id):
            raise ValueError(f"Invalid incident id: {incident_id}")
        self.incidents[incident_id] = incident
        return incident

    # Tool 2 of 3
    def search_knowledge(self, decision: RoutingDecision) -> list[KnowledgeArticle]:
        """Return runbook/SOP knowledge for OPEN_INCIDENT handling."""
        if decision.outcome != RoutingOutcome.OPEN_INCIDENT:
            return []
        title_by_severity = {
            Severity.SEV1: "SEV1 life-safety and statutory response SOP",
            Severity.SEV2: "Major impairment field response runbook",
            Severity.SEV3: "Contained incident triage guide",
            Severity.SEV4: "Customer communications template",
        }
        article = KnowledgeArticle(
            article_id=f"KB-{decision.severity.value}",
            title=title_by_severity[decision.severity],
            snippet=f"{decision.severity.value} incidents use the {decision.target_queue} queue and SLA {decision.sla_minutes} minutes.",
            relevance_score=0.91,
        )
        return [article]

    # Tool 3 of 3
    def generate_sitrep(self, incident: dict[str, Any], decision: RoutingDecision, articles: list[KnowledgeArticle]) -> SitrepDraft:
        """Generate a citation-grounded sitrep from incident and knowledge records."""
        incident_citation = Citation(
            source_id=incident["incident_id"],
            source_type="incident",
            quote=f"{incident['incident_id']} {incident['severity']} {incident['queue']}",
        )
        citations = [incident_citation]
        if articles:
            citations.append(Citation(articles[0].article_id, "kb_article", articles[0].snippet))
        summary = (
            f"Incident {incident['incident_id']} is classified {incident['severity']} "
            f"and assigned to {incident['queue']}."
        )
        return SitrepDraft(incident_id=incident["incident_id"], summary=summary, citations=citations)

    def _sla_text(self, minutes: int) -> str:
        if minutes == 15:
            return "15-minute"
        if minutes == 60:
            return "1-hour"
        if minutes == 240:
            return "4-hour"
        return "next-business-day"


def create_action_agents() -> dict[str, ActionAgent]:
    """Factory retained for lab harnesses; ActionAgent owns exactly three tools."""
    return {"action_agent": ActionAgent()}

