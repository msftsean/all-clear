"""Interfaces for All Clear external services and incident persistence."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional, Protocol, runtime_checkable
from uuid import UUID

from app.agents.schemas import IncidentRecord, KnowledgeArticle, SignalCategory
from app.models.schemas import AuditLog, Session
from app.models.voice_schemas import RealtimeSessionResponse, ToolCallResponse, ToolDefinition


@runtime_checkable
class EmbeddingFn(Protocol):
    async def __call__(self, text: str) -> list[float]: ...


class KnowledgeServiceInterface(ABC):
    @abstractmethod
    async def search(
        self, query: str, department: Optional[str] = None, limit: int = 3
    ) -> list[KnowledgeArticle]: ...

    @abstractmethod
    async def search_with_content(
        self, query: str, department: Optional[str] = None, limit: int = 3
    ) -> tuple[list[KnowledgeArticle], list[dict]]: ...

    @abstractmethod
    async def get_article(self, article_id: str) -> Optional[KnowledgeArticle]: ...

    @abstractmethod
    async def health_check(self) -> tuple[bool, Optional[int], Optional[str]]: ...


class SessionStoreInterface(ABC):
    @abstractmethod
    async def create_session(self, session: Session) -> None: ...

    @abstractmethod
    async def get_session(self, session_id: UUID) -> Optional[Session]: ...

    @abstractmethod
    async def update_session(self, session: Session) -> None: ...

    @abstractmethod
    async def get_sessions_by_student(self, student_id_hash: str, limit: int = 10) -> list[Session]: ...

    @abstractmethod
    async def health_check(self) -> tuple[bool, Optional[int], Optional[str]]: ...


class AuditLogInterface(ABC):
    @abstractmethod
    async def log_interaction(self, audit_log: AuditLog) -> None: ...

    @abstractmethod
    async def get_logs_by_session(self, session_id: UUID) -> list[AuditLog]: ...

    @abstractmethod
    async def get_logs_by_student(self, student_id_hash: str, limit: int = 100) -> list[AuditLog]: ...

    @abstractmethod
    async def health_check(self) -> tuple[bool, Optional[int], Optional[str]]: ...


class RealtimeServiceInterface(ABC):
    @abstractmethod
    async def create_session(
        self, session_id: str, voice: str, instructions: Optional[str] = None
    ) -> RealtimeSessionResponse: ...

    @abstractmethod
    async def get_tool_definitions(self) -> list[ToolDefinition]: ...

    @abstractmethod
    async def execute_tool(
        self, call_id: str, tool_name: str, arguments: dict, session_id: str
    ) -> ToolCallResponse: ...


class PhoneServiceInterface(ABC):
    @abstractmethod
    async def handle_incoming_call(self, incoming_call_context: str, caller_id: str, callback_url: str) -> dict: ...

    @abstractmethod
    async def handle_call_event(self, event_type: str, event_data: dict) -> dict: ...

    @abstractmethod
    async def health_check(self) -> tuple[bool, Optional[int], Optional[str]]: ...


class IncidentStoreInterface(ABC):
    @abstractmethod
    async def create_incident(self, record: IncidentRecord, embedding: list[float]) -> IncidentRecord: ...

    @abstractmethod
    async def attach_report(self, incident_id: str, signal_text: str) -> IncidentRecord: ...

    @abstractmethod
    async def get_incident(self, incident_id: str) -> Optional[IncidentRecord]: ...

    @abstractmethod
    async def get_open_incidents(self, intent_category: SignalCategory) -> list[IncidentRecord]: ...
