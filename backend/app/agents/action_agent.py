"""
ActionAgent: incident creation, knowledge search, and citation-grounded sitreps
(001-maf-rehost, T8).

Bounded Authority (Constitution Art. II + Art. IV):
- CAN: open an incident on the OPEN_INCIDENT path, attach a report on the
  ATTACH_TO_INCIDENT path, search the knowledge base (OPEN path only), and draft a
  situation report in which every claim is backed by a citation.
- CANNOT: classify, route, set severity, or bypass an escalation the RouterExecutor
  decided. It executes the RoutingDecision; it does not second-guess it.

Two surfaces are provided:
- ``build_action_agent`` returns a MAF ``Agent`` (Appendix B) whose tools delegate to
  the injected interfaces. This is the live narrative/tool surface.
- ``ActionExecutor`` is the deterministic workflow stage. Because the offline mock chat
  client does not auto-invoke tools, the executor calls the toolbox directly so mock
  mode and live mode persist identical incidents and audit entries (Constitution Art. V).
"""

# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime, timezone

from agent_framework import Agent, BaseChatClient, Executor, WorkflowContext, handler

from app.agents.envelopes import RoutedSignal
from app.agents.schemas import (
    ActionStatus,
    Citation,
    IncidentAction,
    IncidentRecord,
    IncidentStatus,
    KnowledgeArticle,
    RoutingDecision,
    RoutingOutcome,
    SitrepDraft,
)
from app.core.config import Settings
from app.services.interfaces import (
    EmbeddingFn,
    IncidentStoreInterface,
    KnowledgeServiceInterface,
)

ACTION_AGENT_SYSTEM_PROMPT = """You are the ActionAgent for All Clear, a cross-vertical incident-triage assistant. You execute the RouterExecutor's decision and communicate with the reporter.

Your role:
1. On a NEW incident (OPEN_INCIDENT): confirm the incident id, severity, and target response time; search the knowledge base for relevant guidance; and draft a short situation report (sitrep).
2. On a duplicate report (ATTACH_TO_INCIDENT): give a brief acknowledgment that the report was added to the existing incident, including its current magnitude. Do NOT run a knowledge search on this path — it keeps surge latency flat.

## Grounding and citations (non-negotiable — Constitution Art. IV: truth over fluency)

1. Every factual claim in a sitrep MUST carry a citation to a source record: an incident, a signal, or a knowledge article.
2. Cite knowledge articles as [Source: <article_id>]. Never invent facts or article ids.
3. If the knowledge base has no relevant article, say so plainly rather than fabricating guidance.
4. Never echo PII (SSNs, card numbers, phone numbers) back to the reporter.

## Tone

- Be calm, direct, and solution-focused. Acknowledge urgency without amplifying panic.
- Surge acknowledgments are short: reporters during an incident need confirmation, not prose.

You have these tools: create_incident, search_knowledge, generate_sitrep. Use create_incident only on the OPEN_INCIDENT path; use search_knowledge and generate_sitrep only on the OPEN_INCIDENT path."""


def _sla_phrase(minutes: int) -> str:
    """Human-readable SLA estimate from a minute budget."""
    if minutes <= 15:
        return f"within {minutes} minutes"
    if minutes < 60:
        return f"within {minutes} minutes"
    if minutes < 1440:
        hours = minutes // 60
        return f"within {hours} hour{'s' if hours != 1 else ''}"
    days = minutes // 1440
    return "by next business day" if days <= 1 else f"within {days} business days"


class ActionToolbox:
    """Tools that delegate to the injected interfaces. Audit logging is performed by
    the IncidentStore on every create/mutate (Constitution Art. I.3)."""

    def __init__(
        self,
        store: IncidentStoreInterface,
        knowledge: KnowledgeServiceInterface,
        embed: EmbeddingFn,
        settings: Settings,
    ) -> None:
        self._store = store
        self._knowledge = knowledge
        self._embed = embed
        self._settings = settings

    async def create_incident(
        self, record: IncidentRecord, embedding: list[float]
    ) -> IncidentRecord:
        """Persist a new incident and its dedup embedding (OPEN_INCIDENT path)."""
        return await self._store.create_incident(record, embedding)

    async def attach_report(self, incident_id: str, signal_text: str) -> IncidentRecord:
        """Attach a duplicate signal as a report to an existing incident (ATTACH path)."""
        return await self._store.attach_report(incident_id, signal_text)

    async def search_knowledge(self, query: str) -> list[KnowledgeArticle]:
        """Search the knowledge base; return articles at or above the relevance floor."""
        results = await self._knowledge.search(query=query, department=None, limit=3)
        articles: list[KnowledgeArticle] = []
        for art in results:
            if art.relevance_score < self._settings.kb_relevance_threshold:
                continue
            articles.append(
                KnowledgeArticle(
                    article_id=art.article_id,
                    title=art.title,
                    url=art.url,
                    snippet=art.snippet,
                    relevance_score=art.relevance_score,
                )
            )
        return articles

    async def generate_sitrep(
        self, incident: IncidentRecord, articles: list[KnowledgeArticle]
    ) -> SitrepDraft:
        """Draft a citation-grounded sitrep. Every claim cites a source record."""
        citations = [
            Citation(
                source_id=incident.incident_id,
                source_type="incident",
                quote=incident.summary,
            )
        ]
        for art in articles:
            citations.append(
                Citation(
                    source_id=art.article_id,
                    source_type="kb_article",
                    quote=art.snippet or art.title,
                )
            )
        summary = (
            f"{incident.severity.value} incident {incident.incident_id} opened on "
            f"{incident.queue.value} [Source: {incident.incident_id}]."
        )
        if articles:
            refs = "; ".join(f"{a.title} [Source: {a.article_id}]" for a in articles)
            summary += f" Relevant guidance: {refs}."
        return SitrepDraft(
            incident_id=incident.incident_id, summary=summary, citations=citations
        )


def build_action_agent(client: BaseChatClient, toolbox: ActionToolbox) -> Agent:
    """Build the All Clear ActionAgent as a MAF Agent with tools bound to *toolbox*.

    The tools delegate to the injected IncidentStore and KnowledgeService interfaces.
    In live mode the model may invoke them; the deterministic workflow path uses
    ``ActionExecutor`` which calls the same toolbox directly.
    """
    return Agent(
        client,
        ACTION_AGENT_SYSTEM_PROMPT,
        name="ActionAgent",
        description="Opens/attaches incidents, searches knowledge, and drafts cited sitreps.",
        tools=[
            toolbox.create_incident,
            toolbox.search_knowledge,
            toolbox.generate_sitrep,
        ],
    )


class ActionExecutor(Executor):
    """Deterministic ActionAgent workflow stage. Executes the RoutingDecision."""

    def __init__(
        self,
        toolbox: ActionToolbox,
        store: IncidentStoreInterface,
        *,
        id: str = "action",
    ) -> None:
        super().__init__(id=id)
        self._tools = toolbox
        self._store = store

    @handler
    async def act(
        self, message: RoutedSignal, ctx: WorkflowContext[IncidentAction, IncidentAction]
    ) -> None:
        action = await self.run_action(message)
        await ctx.send_message(action)
        await ctx.yield_output(action)

    async def run_action(self, routed: RoutedSignal) -> IncidentAction:
        decision = routed.routing
        if decision.outcome is RoutingOutcome.ATTACH_TO_INCIDENT:
            return await self._handle_attach(routed)
        return await self._handle_open(routed)

    async def _handle_open(self, routed: RoutedSignal) -> IncidentAction:
        decision: RoutingDecision = routed.routing
        incident_id = await self._store.next_incident_id()
        record = IncidentRecord(
            incident_id=incident_id,
            queue=decision.target_queue,
            severity=decision.severity,
            status=IncidentStatus.OPEN,  # stay open so dedup keeps matching the cluster
            summary=self._summarize(routed),
            intent_category=routed.classification.intent_category,
            magnitude=1,
            sla_minutes=decision.sla_minutes,
            created_at=datetime.now(timezone.utc),
            escalated=decision.escalate,
        )
        await self._tools.create_incident(record, routed.embedding)

        # Knowledge search + sitrep happen ONLY on the OPEN path (spec clarification #3).
        articles = await self._tools.search_knowledge(routed.signal_text)
        sitrep = await self._tools.generate_sitrep(record, articles)

        eta = _sla_phrase(decision.sla_minutes)
        status = ActionStatus.ESCALATED if decision.escalate else ActionStatus.OPENED
        message = (
            f"Logged incident {incident_id} ({decision.severity.value}) on the "
            f"{decision.target_queue.value} queue; target response {eta}."
        )
        if decision.escalate:
            reason = decision.escalation_reason.value if decision.escalation_reason else "review"
            message += f" Escalated to a human ({reason})."
        if articles:
            message += " " + "; ".join(
                f"See {a.title} [Source: {a.article_id}]" for a in articles
            )
        return IncidentAction(
            status=status,
            incident_id=incident_id,
            queue=decision.target_queue,
            severity=decision.severity,
            knowledge_articles=articles,
            sitrep=sitrep,
            citations=sitrep.citations,
            estimated_response_time=eta,
            escalated=decision.escalate,
            user_message=message,
        )

    async def _handle_attach(self, routed: RoutedSignal) -> IncidentAction:
        decision = routed.routing
        incident_id = decision.matched_incident_id
        assert incident_id is not None  # guaranteed by RoutingDecision validator
        record = await self._tools.attach_report(incident_id, routed.signal_text)
        eta = _sla_phrase(record.sla_minutes)
        # Short acknowledgment, NO knowledge search (keeps surge latency flat).
        message = (
            f"Thanks — your report was added to incident {incident_id}, now with "
            f"{record.magnitude} reports. Crews are already engaged; target response {eta}."
        )
        return IncidentAction(
            status=ActionStatus.ATTACHED,
            incident_id=incident_id,
            queue=record.queue,
            severity=record.severity,
            knowledge_articles=[],
            sitrep=None,
            citations=[
                Citation(
                    source_id=incident_id,
                    source_type="incident",
                    quote=record.summary,
                )
            ],
            estimated_response_time=eta,
            escalated=record.escalated,
            user_message=message,
        )

    @staticmethod
    def _summarize(routed: RoutedSignal) -> str:
        cls = routed.classification
        loc = cls.entities.location
        base = cls.intent.replace("_", " ").capitalize()
        if loc:
            base += f" at {loc}"
        return base[:200]
