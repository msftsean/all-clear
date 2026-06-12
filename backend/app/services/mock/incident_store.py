"""
In-memory mock incident store (001-maf-rehost, T6).

Offline twin of the Cosmos `incidents` container (spec clarification #2). Stores
incidents, their dedup embeddings, and an audit trail of create/mutate operations
(Constitution Art. I.3). Mock and live stay in lockstep behind IncidentStoreInterface.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

from app.agents.schemas import (
    IncidentRecord,
    IncidentStatus,
    SignalCategory,
)
from app.services.interfaces import IncidentStoreInterface


class AuditEntry:
    """Lightweight audit record (actor, action, target, cause, timestamp)."""

    def __init__(self, actor: str, action: str, target: str, cause: str) -> None:
        self.actor = actor
        self.action = action
        self.target = target
        self.cause = cause
        self.timestamp = datetime.now(timezone.utc)

    def __repr__(self) -> str:  # pragma: no cover - debug aid
        return f"AuditEntry({self.actor} {self.action} {self.target}: {self.cause})"


class MockIncidentStore(IncidentStoreInterface):
    """In-memory IncidentStore for mock mode and tests.

    Bounded authority: persistence only. No classification/routing/escalation.
    Instances are independent so tests do not leak state into one another.
    """

    def __init__(self) -> None:
        self._incidents: dict[str, IncidentRecord] = {}
        self._embeddings: dict[str, list[float]] = {}
        self._reports: dict[str, list[str]] = {}
        self.audit: list[AuditEntry] = []
        self._seq = 0

    async def next_incident_id(self) -> str:
        self._seq += 1
        return f"AC-{self._seq:04d}"

    async def create_incident(
        self, record: IncidentRecord, embedding: list[float]
    ) -> IncidentRecord:
        self._incidents[record.incident_id] = record
        self._embeddings[record.incident_id] = list(embedding)
        self._reports[record.incident_id] = []
        self.audit.append(
            AuditEntry(
                actor="ActionAgent.create_incident",
                action="create",
                target=record.incident_id,
                cause=f"OPEN_INCIDENT severity={record.severity.value} queue={record.queue.value}",
            )
        )
        return record

    async def attach_report(self, incident_id: str, signal_text: str) -> IncidentRecord:
        record = self._incidents.get(incident_id)
        if record is None:
            raise KeyError(f"unknown incident {incident_id}")
        # Preserve every signal; dedup attaches, never deletes (Constitution Art. V.4).
        self._reports[incident_id].append(signal_text)
        record.magnitude += 1
        record.updated_at = datetime.now(timezone.utc)
        self.audit.append(
            AuditEntry(
                actor="ActionAgent.attach_report",
                action="attach",
                target=incident_id,
                cause=f"ATTACH_TO_INCIDENT magnitude={record.magnitude}",
            )
        )
        return record

    async def get_incident(self, incident_id: str) -> Optional[IncidentRecord]:
        return self._incidents.get(incident_id)

    async def get_open_incidents(
        self, intent_category: SignalCategory
    ) -> list[IncidentRecord]:
        return [
            r
            for r in self._incidents.values()
            if r.status is IncidentStatus.OPEN and r.intent_category is intent_category
        ]

    async def get_open_incident_vectors(
        self, intent_category: SignalCategory
    ) -> list[tuple[str, list[float]]]:
        open_ids = {r.incident_id for r in await self.get_open_incidents(intent_category)}
        return [(iid, vec) for iid, vec in self._embeddings.items() if iid in open_ids]

    def report_count(self, incident_id: str) -> int:
        """Number of attached reports (test/inspection helper)."""
        return len(self._reports.get(incident_id, []))
