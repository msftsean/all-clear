"""
All Clear Lab 05 pipeline scaffold.

Flow: signal -> QueryAgent -> RouterExecutor -> ActionAgent -> IncidentAction.
"""

from __future__ import annotations

import logging
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional

from action_agent import ActionAgent, IncidentAction
from query_agent import QueryAgent, SignalClassification
from router_agent import OpenIncident, RouterExecutor

logger = logging.getLogger(__name__)


@dataclass
class ConversationTurn:
    """One preserved inbound signal and ActionAgent response."""

    turn_id: str
    timestamp: datetime
    signal_text: str
    agent_response: str
    category: str
    entities: dict
    outcome: str
    confidence: float


@dataclass
class Session:
    """Maintains channel/session state across turns."""

    session_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    turns: list[ConversationTurn] = field(default_factory=list)
    context: dict = field(default_factory=dict)

    def add_turn(
        self,
        signal_text: str,
        agent_response: str,
        category: str,
        entities: dict,
        outcome: str,
        confidence: float,
    ) -> ConversationTurn:
        turn = ConversationTurn(
            turn_id=str(uuid.uuid4()),
            timestamp=datetime.now(timezone.utc),
            signal_text=signal_text,
            agent_response=agent_response,
            category=category,
            entities=entities,
            outcome=outcome,
            confidence=confidence,
        )
        self.turns.append(turn)
        self.context.setdefault("all_entities", {}).update(entities)
        return turn

    def get_history(self, max_turns: int = 5) -> list[dict]:
        recent = self.turns[-max_turns:]
        history: list[dict] = []
        for turn in recent:
            history.append({"role": "user", "content": turn.signal_text})
            history.append({"role": "assistant", "content": turn.agent_response})
        return history

    def get_context_summary(self) -> str:
        if not self.turns:
            return "No previous signals in this session."
        categories = sorted({turn.category for turn in self.turns[-3:]})
        entities = self.context.get("all_entities", {})
        return f"Recent categories: {', '.join(categories)}\nKnown entities: {entities}\nSignal count: {len(self.turns)}"


class SessionManager:
    """In-memory session manager for the lab mini-app."""

    def __init__(self) -> None:
        self._sessions: dict[str, Session] = {}

    def get_or_create(self, session_id: Optional[str] = None) -> Session:
        if session_id and session_id in self._sessions:
            return self._sessions[session_id]
        session = Session(session_id=session_id) if session_id else Session()
        self._sessions[session.session_id] = session
        return session

    def get(self, session_id: str) -> Optional[Session]:
        return self._sessions.get(session_id)

    def delete(self, session_id: str) -> bool:
        return self._sessions.pop(session_id, None) is not None


class AgentPipeline:
    """Coordinates QueryAgent, RouterExecutor, and ActionAgent."""

    def __init__(
        self,
        query_agent: Optional[QueryAgent] = None,
        router_executor: Optional[RouterExecutor] = None,
        action_agent: Optional[ActionAgent] = None,
        open_incidents: Optional[list[OpenIncident]] = None,
        openai_client=None,
        model_deployment: str = "gpt-5.1",
    ) -> None:
        self.session_manager = SessionManager()
        self.query_agent = query_agent or QueryAgent(client=openai_client, model=model_deployment)
        self.router_executor = router_executor or RouterExecutor(open_incidents=open_incidents)
        self.action_agent = action_agent or ActionAgent()

    async def process(self, signal_text: str, session_id: Optional[str] = None) -> tuple[IncidentAction, str]:
        if not signal_text or not signal_text.strip():
            session = self.session_manager.get_or_create(session_id)
            return IncidentAction(
                status="error",
                incident_id=None,
                queue="customer-comms",
                severity=self.router_executor._severity(  # uses GENERAL_INQUIRY fallback classification
                    SignalClassification(signal_text="empty", category=__import__("query_agent").SignalCategory.GENERAL_INQUIRY, confidence=0.0)
                ),
                estimated_response_time="next-business-day",
                user_message="No signal was received. Please send the location and what is happening.",
                requires_followup=True,
                confidence=0.0,
            ), session.session_id

        session = self.session_manager.get_or_create(session_id)
        # TODO: Wire QueryAgent -> RouterExecutor -> ActionAgent in this order.
        classification = await self.query_agent.classify(signal_text, session.get_context_summary())
        decision = await self.router_executor.route(classification, signal_text)
        action = await self.action_agent.execute(decision, session.get_history())
        session.add_turn(
            signal_text=signal_text,
            agent_response=action.user_message,
            category=classification.category.value,
            entities=classification.entities.as_dict(),
            outcome=decision.outcome.value,
            confidence=classification.confidence,
        )
        logger.info("Processed signal category=%s outcome=%s", classification.category.value, decision.outcome.value)
        return action, session.session_id

    def add_open_incident(self, incident: OpenIncident) -> None:
        self.router_executor.add_open_incident(incident)
