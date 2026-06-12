"""Tests for AzureCosmosIncidentStore against an in-memory fake container.

Runs the same behavioral scenarios as test_incident_store_interface.py (the mock
suite) so the live Cosmos store stays in lockstep with MockIncidentStore
(spec 016-production-deployment, D1 acceptance) without needing a live Cosmos
account. The fake container mimics the async Cosmos ContainerProxy surface the
store depends on, including etag optimistic concurrency.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any, AsyncIterator, Optional

import pytest

from app.agents.schemas import (
    IncidentRecord,
    IncidentStatus,
    Queue,
    Severity,
    SignalCategory,
)
from app.services.azure.incident_store import AzureCosmosIncidentStore
from app.services.interfaces import IncidentStoreInterface


class FakeCosmosContainer:
    """Minimal in-memory async stand-in for a Cosmos ContainerProxy."""

    def __init__(self) -> None:
        # keyed by (partition_value, id) -> document (includes _etag)
        self._items: dict[tuple[str, str], dict[str, Any]] = {}

    @staticmethod
    def _partition(doc: dict[str, Any]) -> str:
        return str(doc["intent_category"])

    def _stamp(self, doc: dict[str, Any]) -> dict[str, Any]:
        stored = dict(doc)
        stored["_etag"] = f'"{uuid.uuid4().hex}"'
        self._items[(self._partition(stored), stored["id"])] = stored
        return dict(stored)

    async def create_item(self, body: dict[str, Any]) -> dict[str, Any]:
        from azure.cosmos.exceptions import CosmosResourceExistsError

        key = (self._partition(body), body["id"])
        if key in self._items:
            raise CosmosResourceExistsError(message="exists")
        return self._stamp(body)

    async def read_item(self, item: str, partition_key: str) -> dict[str, Any]:
        from azure.cosmos.exceptions import CosmosResourceNotFoundError

        stored = self._items.get((str(partition_key), item))
        if stored is None:
            raise CosmosResourceNotFoundError(message="not found")
        return dict(stored)

    async def replace_item(
        self,
        item: str,
        body: dict[str, Any],
        etag: Optional[str] = None,
        match_condition: Any = None,
    ) -> dict[str, Any]:
        from azure.cosmos.exceptions import (
            CosmosAccessConditionFailedError,
            CosmosResourceNotFoundError,
        )

        key = (self._partition(body), item)
        stored = self._items.get(key)
        if stored is None:
            raise CosmosResourceNotFoundError(message="not found")
        if etag is not None and stored["_etag"] != etag:
            raise CosmosAccessConditionFailedError(message="etag mismatch")
        return self._stamp(body)

    async def query_items(
        self,
        query: str,
        parameters: list[dict[str, Any]],
        enable_cross_partition_query: bool = False,
        partition_key: Optional[str] = None,
    ) -> AsyncIterator[dict[str, Any]]:
        params = {p["name"]: p["value"] for p in parameters}
        for (partition, _id), doc in list(self._items.items()):
            if "@id" in params and doc.get("id") != params["@id"]:
                continue
            if "@cat" in params and doc.get("intent_category") != params["@cat"]:
                continue
            if partition_key is not None and partition != str(partition_key):
                continue
            yield dict(doc)


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


@pytest.fixture
def store() -> AzureCosmosIncidentStore:
    return AzureCosmosIncidentStore(FakeCosmosContainer())


def test_cosmos_store_is_incident_store(store: AzureCosmosIncidentStore) -> None:
    assert isinstance(store, IncidentStoreInterface)


async def test_next_id_is_monotonic(store: AzureCosmosIncidentStore) -> None:
    assert await store.next_incident_id() == "AC-0001"
    assert await store.next_incident_id() == "AC-0002"
    assert await store.next_incident_id() == "AC-0003"


async def test_create_and_get(store: AzureCosmosIncidentStore) -> None:
    iid = await store.next_incident_id()
    assert iid == "AC-0001"
    rec = await store.create_incident(
        _record(iid, SignalCategory.INFRASTRUCTURE_OUTAGE), [0.1, 0.2]
    )
    assert (await store.get_incident(iid)) == rec
    assert len(store.audit) == 1
    assert store.audit[0].action == "create"


async def test_get_missing_returns_none(store: AzureCosmosIncidentStore) -> None:
    assert await store.get_incident("AC-9999") is None


async def test_attach_increments_magnitude_and_preserves_signal(
    store: AzureCosmosIncidentStore,
) -> None:
    iid = await store.next_incident_id()
    await store.create_incident(_record(iid, SignalCategory.INFRASTRUCTURE_OUTAGE), [0.1])
    updated = await store.attach_report(iid, "another report of the same outage")
    assert updated.magnitude == 2
    assert await store.report_count(iid) == 1  # signal preserved, never deleted
    assert store.audit[-1].action == "attach"


async def test_attach_unknown_incident_raises(store: AzureCosmosIncidentStore) -> None:
    with pytest.raises(KeyError):
        await store.attach_report("AC-0001", "ghost")


async def test_open_incidents_scoped_by_category(
    store: AzureCosmosIncidentStore,
) -> None:
    a = await store.next_incident_id()
    b = await store.next_incident_id()
    await store.create_incident(_record(a, SignalCategory.INFRASTRUCTURE_OUTAGE), [1.0, 0.0])
    await store.create_incident(_record(b, SignalCategory.CUSTOMER_INQUIRY), [0.0, 1.0])
    outage = await store.get_open_incidents(SignalCategory.INFRASTRUCTURE_OUTAGE)
    assert [r.incident_id for r in outage] == [a]
    vectors = await store.get_open_incident_vectors(SignalCategory.INFRASTRUCTURE_OUTAGE)
    assert vectors == [(a, [1.0, 0.0])]


async def test_resolved_incidents_excluded_from_dedup(
    store: AzureCosmosIncidentStore,
) -> None:
    iid = await store.next_incident_id()
    rec = _record(iid, SignalCategory.INFRASTRUCTURE_OUTAGE)
    rec.status = IncidentStatus.RESOLVED
    await store.create_incident(rec, [1.0])
    assert await store.get_open_incident_vectors(SignalCategory.INFRASTRUCTURE_OUTAGE) == []


async def test_counter_doc_excluded_from_category_query(
    store: AzureCosmosIncidentStore,
) -> None:
    # Allocating ids creates the counter doc; it must never leak into dedup scope.
    await store.next_incident_id()
    iid = await store.next_incident_id()
    await store.create_incident(_record(iid, SignalCategory.INFRASTRUCTURE_OUTAGE), [1.0])
    open_incidents = await store.get_open_incidents(SignalCategory.INFRASTRUCTURE_OUTAGE)
    assert [r.incident_id for r in open_incidents] == [iid]
