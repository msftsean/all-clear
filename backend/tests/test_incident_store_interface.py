"""Tests for the incident store interface + mock (001-maf-rehost, T6)."""

from datetime import datetime, timezone

import pytest

from app.agents.schemas import (
    IncidentRecord,
    IncidentStatus,
    Queue,
    Severity,
    SignalCategory,
)
from app.services.interfaces import EmbeddingFn, IncidentStoreInterface
from app.services.mock.incident_store import MockIncidentStore


def _record(store_id: str, category: SignalCategory) -> IncidentRecord:
    return IncidentRecord(
        incident_id=store_id,
        queue=Queue.ENGINEERING,
        severity=Severity.SEV2,
        summary="outage",
        intent_category=category,
        sla_minutes=60,
        created_at=datetime.now(timezone.utc),
    )


def test_mock_is_incident_store() -> None:
    assert isinstance(MockIncidentStore(), IncidentStoreInterface)


async def test_create_and_get() -> None:
    store = MockIncidentStore()
    iid = await store.next_incident_id()
    assert iid == "AC-0001"
    rec = await store.create_incident(_record(iid, SignalCategory.INFRASTRUCTURE_OUTAGE), [0.1, 0.2])
    assert (await store.get_incident(iid)) == rec
    assert len(store.audit) == 1
    assert store.audit[0].action == "create"


async def test_attach_increments_magnitude_and_preserves_signal() -> None:
    store = MockIncidentStore()
    iid = await store.next_incident_id()
    await store.create_incident(_record(iid, SignalCategory.INFRASTRUCTURE_OUTAGE), [0.1])
    updated = await store.attach_report(iid, "another report of the same outage")
    assert updated.magnitude == 2
    assert store.report_count(iid) == 1  # signal preserved, never deleted
    assert store.audit[-1].action == "attach"


async def test_open_incidents_scoped_by_category() -> None:
    store = MockIncidentStore()
    a = await store.next_incident_id()
    b = await store.next_incident_id()
    await store.create_incident(_record(a, SignalCategory.INFRASTRUCTURE_OUTAGE), [1.0, 0.0])
    await store.create_incident(_record(b, SignalCategory.CUSTOMER_INQUIRY), [0.0, 1.0])
    outage = await store.get_open_incidents(SignalCategory.INFRASTRUCTURE_OUTAGE)
    assert [r.incident_id for r in outage] == [a]
    vectors = await store.get_open_incident_vectors(SignalCategory.INFRASTRUCTURE_OUTAGE)
    assert vectors == [(a, [1.0, 0.0])]


async def test_resolved_incidents_excluded_from_dedup() -> None:
    store = MockIncidentStore()
    iid = await store.next_incident_id()
    rec = _record(iid, SignalCategory.INFRASTRUCTURE_OUTAGE)
    rec.status = IncidentStatus.RESOLVED
    await store.create_incident(rec, [1.0])
    assert await store.get_open_incident_vectors(SignalCategory.INFRASTRUCTURE_OUTAGE) == []


async def test_embedding_fn_protocol_runtime_checkable() -> None:
    async def embed(text: str) -> list[float]:
        return [float(len(text))]

    assert isinstance(embed, EmbeddingFn)
    assert await embed("abc") == [3.0]
