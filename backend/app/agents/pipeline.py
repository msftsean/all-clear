"""
AllClearPipeline: chain QueryAgent -> RouterExecutor -> ActionExecutor (001-maf-rehost, T9).

Wiring:
- ``build_workflow`` assembles the canonical MAF ``WorkflowBuilder`` chain
  (QueryStage -> RouterExecutor -> ActionExecutor) for live/streamed execution.
- ``AllClearPipeline.process_signal`` is the adapter the API and voice tool path call:
  text in -> typed ``PipelineResult`` out, publishing SSE lifecycle events onto the
  existing ``transcript_bus`` at each stage so the ClearBoard updates live.

The pipeline keeps the three stages as the single source of truth, so the workflow path
and the adapter path produce identical incidents and audit entries (Constitution Art. V).
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Any, Optional

from agent_framework import (
    Agent,
    ChatOptions,
    Executor,
    Workflow,
    WorkflowBuilder,
    WorkflowContext,
    handler,
)

from app.agents.action_agent import ActionExecutor, ActionToolbox
from app.agents.envelopes import ClassifiedSignal, RoutedSignal
from app.agents.query_agent import build_query_agent
from app.agents.router_agent import RouterExecutor
from app.agents.schemas import (
    IncidentAction,
    PipelineResult,
    RoutingOutcome,
    SignalClassification,
)
from app.core.config import Settings, get_settings
from app.services.mock.embeddings import mock_embed
from app.services.mock.incident_store import MockIncidentStore
from app.services.mock.knowledge_service import MockKnowledgeService
from app.services.mock.maf_chat_client import MockChatClient
from app.services.pii import redact_pii_text
from app.services.transcript_bus import transcript_bus


@dataclass
class InboundSignal:
    """Raw inbound signal entering the workflow."""

    text: str
    session_id: str = "anonymous"
    channel: str = "chat"


class QueryStage(Executor):
    """Workflow entry stage: runs the QueryAgent and emits a ClassifiedSignal."""

    def __init__(self, agent: Agent, *, id: str = "query") -> None:
        super().__init__(id=id)
        self._agent = agent

    @handler
    async def classify(
        self, message: InboundSignal, ctx: WorkflowContext[ClassifiedSignal]
    ) -> None:
        classification = await classify_signal(self._agent, message.text)
        await ctx.send_message(
            ClassifiedSignal(
                signal_text=message.text,
                classification=classification,
                session_id=message.session_id,
                channel=message.channel,
            )
        )


async def classify_signal(agent: Agent, text: str) -> SignalClassification:
    """Run the QueryAgent and return its typed SignalClassification."""
    response = await agent.run(
        text, options=ChatOptions(response_format=SignalClassification)
    )
    value = response.value
    if not isinstance(value, SignalClassification):  # pragma: no cover - defensive
        raise TypeError(f"QueryAgent returned {type(value)!r}, expected SignalClassification")
    return value


def build_workflow(
    query_agent: Agent, router: RouterExecutor, action: ActionExecutor
) -> Workflow:
    """Assemble the canonical QueryStage -> Router -> Action workflow chain."""
    query_stage = QueryStage(query_agent)
    return (
        WorkflowBuilder(start_executor=query_stage, output_from=[action])
        .add_chain([query_stage, router, action])
        .build()
    )


class AllClearPipeline:
    """Adapter over the three-stage chain with SSE lifecycle publication."""

    def __init__(
        self,
        query_agent: Agent,
        router: RouterExecutor,
        action: ActionExecutor,
        *,
        store: MockIncidentStore | None = None,
        bus: Any = transcript_bus,
    ) -> None:
        self._query_agent = query_agent
        self._router = router
        self._action = action
        self._bus = bus
        self.store = store
        self.workflow = build_workflow(query_agent, router, action)

    async def process_signal(
        self,
        text: str,
        session_id: str = "anonymous",
        channel: str = "chat",
    ) -> PipelineResult:
        """Run text through classify -> route -> act, publishing events per stage."""
        started = time.perf_counter()

        # Classify on the raw text so the QueryAgent can still detect/flag PII
        # (pii_detected/pii_types stay accurate for routing). After classification
        # the raw text is dropped: every downstream use (dedup embedding, attached
        # report persistence, and the returned PipelineResult) sees only the
        # redacted text, so PII is never echoed back or stored at rest.
        # This mirrors the voice path (realtime.py redact_pii on ingress/egress)
        # and satisfies Constitution Art. I.1 + voice/text lockstep (Art. V.1).
        classification = await classify_signal(self._query_agent, text)
        safe_text = redact_pii_text(text)
        await self._publish(
            session_id,
            {
                "type": "signal.classified",
                "channel": channel,
                "intent_category": classification.intent_category.value,
                "confidence": classification.confidence,
            },
        )

        decision, embedding = await self._router.decide(safe_text, classification)
        await self._publish(
            session_id,
            {
                "type": "signal.routed",
                "outcome": decision.outcome.value,
                "severity": decision.severity.value,
                "queue": decision.target_queue.value,
                "matched_incident_id": decision.matched_incident_id,
                "escalate": decision.escalate,
            },
        )

        routed = RoutedSignal(
            signal_text=safe_text,
            classification=classification,
            routing=decision,
            embedding=embedding,
            session_id=session_id,
            channel=channel,
        )
        action: IncidentAction = await self._action.run_action(routed)
        await self._publish(
            session_id,
            {
                "type": (
                    "incident.attached"
                    if decision.outcome is RoutingOutcome.ATTACH_TO_INCIDENT
                    else "incident.opened"
                ),
                "incident_id": action.incident_id,
                "severity": action.severity.value,
                "queue": action.queue.value,
                "escalated": action.escalated,
            },
        )

        elapsed_ms = int((time.perf_counter() - started) * 1000)
        result = PipelineResult(
            session_id=session_id,
            channel=channel,
            signal_text=safe_text,
            classification=classification,
            routing=decision,
            action=action,
            processing_ms=elapsed_ms,
        )
        await self._publish(
            session_id, {"type": "pipeline.complete", "processing_ms": elapsed_ms}
        )
        return result

    async def _publish(self, session_id: str, event: dict[str, Any]) -> None:
        if self._bus is None:
            return
        payload = {"session_id": session_id, **event}
        await self._bus.publish(payload)


def build_mock_pipeline(settings: Optional[Settings] = None) -> AllClearPipeline:
    """Construct a fully offline pipeline (mock client, store, knowledge, embeddings)."""
    cfg = settings or get_settings()
    client = MockChatClient()
    store = MockIncidentStore()
    knowledge = MockKnowledgeService()
    query_agent = build_query_agent(client)
    router = RouterExecutor(mock_embed, store, cfg)
    toolbox = ActionToolbox(store, knowledge, mock_embed, cfg)
    action = ActionExecutor(toolbox, store)
    return AllClearPipeline(query_agent, router, action, store=store)
