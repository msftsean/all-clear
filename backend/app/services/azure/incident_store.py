"""
Azure Cosmos DB incident store (spec 016-production-deployment, D1/FR-1).

Live twin of MockIncidentStore. Persists incidents, their dedup embeddings, and
attached report signals in a Cosmos DB for NoSQL container partitioned by
``/intent_category`` (= the dedup scope RouterExecutor compares within).

Bounded authority (Constitution Art. II): persistence only. No classification,
routing, or escalation. Every create/mutate is audit-logged by this store with
actor, action, target, and cause (Constitution Art. I.3); dedup attaches and
never deletes a signal (Constitution Art. V.4).

The store depends only on an async Cosmos container proxy (``create_item``,
``read_item``, ``replace_item``, ``query_items``) so it can be unit-tested with an
in-memory fake and never requires a live Cosmos account offline. Use
``AzureCosmosIncidentStore.from_settings`` to build the live, credentialed store.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Optional

from app.agents.schemas import IncidentRecord, IncidentStatus, SignalCategory
from app.services.interfaces import IncidentStoreInterface

# Counter document lives in its own logical partition so it is never returned by
# category-scoped dedup queries against real SignalCategory partitions.
_COUNTER_PARTITION = "__counter__"
_COUNTER_ID = "__incident_seq__"
# Fields the store manages on the persisted document but that are not part of the
# IncidentRecord schema. Stripped before reconstructing the record.
_NON_RECORD_FIELDS = {"id", "embedding", "reports"}
_MAX_CAS_RETRIES = 8


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


class AzureCosmosIncidentStore(IncidentStoreInterface):
    """IncidentStore backed by an Azure Cosmos DB for NoSQL container.

    Args:
        container: An async Cosmos ``ContainerProxy`` (or an in-memory fake with
            the same surface) for the ``incidents`` container, partitioned on
            ``/intent_category``.
    """

    def __init__(self, container: Any) -> None:
        self._container = container
        self.audit: list[AuditEntry] = []

    # ------------------------------------------------------------------ #
    # Live factory
    # ------------------------------------------------------------------ #
    @classmethod
    def from_settings(cls, settings: Any) -> "AzureCosmosIncidentStore":
        """Build a live, credentialed store from application settings.

        Uses the account key when configured, otherwise falls back to managed
        identity / DefaultAzureCredential (Constitution: passwordless preferred).
        Imports are lazy so mock mode never needs the Cosmos SDK or credentials.
        """
        from azure.cosmos.aio import CosmosClient

        endpoint = settings.cosmos_db_endpoint
        key = getattr(settings, "cosmos_db_key", "") or ""
        if key:
            client = CosmosClient(endpoint, credential=key)
        else:
            from azure.identity.aio import DefaultAzureCredential

            client = CosmosClient(endpoint, credential=DefaultAzureCredential())

        database = client.get_database_client(settings.cosmos_db_database)
        container_name = getattr(
            settings, "cosmos_db_incidents_container", "incidents"
        )
        container = database.get_container_client(container_name)
        return cls(container)

    # ------------------------------------------------------------------ #
    # Serialization helpers
    # ------------------------------------------------------------------ #
    @staticmethod
    def _to_document(
        record: IncidentRecord, embedding: list[float], reports: list[str]
    ) -> dict[str, Any]:
        doc = record.model_dump(mode="json")
        # Partition key path is /intent_category; model_dump already emits the
        # category as its string value, which Cosmos uses as the partition value.
        doc["id"] = record.incident_id
        doc["embedding"] = list(embedding)
        doc["reports"] = list(reports)
        return doc

    @staticmethod
    def _to_record(doc: dict[str, Any]) -> IncidentRecord:
        fields = {
            k: v
            for k, v in doc.items()
            if not k.startswith("_") and k not in _NON_RECORD_FIELDS
        }
        return IncidentRecord(**fields)

    # ------------------------------------------------------------------ #
    # Interface
    # ------------------------------------------------------------------ #
    async def next_incident_id(self) -> str:
        """Allocate the next monotonic ``AC-####`` id via a CAS counter doc."""
        from azure.core import MatchConditions
        from azure.cosmos.exceptions import (
            CosmosResourceExistsError,
            CosmosResourceNotFoundError,
        )

        for _ in range(_MAX_CAS_RETRIES):
            try:
                doc = await self._container.read_item(
                    item=_COUNTER_ID, partition_key=_COUNTER_PARTITION
                )
            except CosmosResourceNotFoundError:
                seed = {
                    "id": _COUNTER_ID,
                    "intent_category": _COUNTER_PARTITION,
                    "seq": 1,
                }
                try:
                    await self._container.create_item(seed)
                    return "AC-0001"
                except CosmosResourceExistsError:
                    continue  # another worker seeded it; re-read and increment
            else:
                next_seq = int(doc["seq"]) + 1
                doc["seq"] = next_seq
                try:
                    await self._container.replace_item(
                        item=_COUNTER_ID,
                        body=doc,
                        etag=doc.get("_etag"),
                        match_condition=MatchConditions.IfNotModified,
                    )
                    return f"AC-{next_seq:04d}"
                except _precondition_failures():
                    continue  # lost the race; retry with a fresh read
        raise RuntimeError("next_incident_id exceeded CAS retry budget")

    async def create_incident(
        self, record: IncidentRecord, embedding: list[float]
    ) -> IncidentRecord:
        await self._container.create_item(self._to_document(record, embedding, []))
        self.audit.append(
            AuditEntry(
                actor="ActionAgent.create_incident",
                action="create",
                target=record.incident_id,
                cause=(
                    f"OPEN_INCIDENT severity={record.severity.value} "
                    f"queue={record.queue.value}"
                ),
            )
        )
        return record

    async def attach_report(self, incident_id: str, signal_text: str) -> IncidentRecord:
        from azure.core import MatchConditions

        for _ in range(_MAX_CAS_RETRIES):
            doc = await self._find_doc(incident_id)
            if doc is None:
                raise KeyError(f"unknown incident {incident_id}")
            # Preserve every signal; dedup attaches, never deletes (Art. V.4).
            doc.setdefault("reports", []).append(signal_text)
            doc["magnitude"] = int(doc.get("magnitude", 1)) + 1
            doc["updated_at"] = datetime.now(timezone.utc).isoformat()
            try:
                updated = await self._container.replace_item(
                    item=doc["id"],
                    body=doc,
                    etag=doc.get("_etag"),
                    match_condition=MatchConditions.IfNotModified,
                )
            except _precondition_failures():
                continue  # concurrent attach; re-read and retry
            record = self._to_record(updated if updated is not None else doc)
            self.audit.append(
                AuditEntry(
                    actor="ActionAgent.attach_report",
                    action="attach",
                    target=incident_id,
                    cause=f"ATTACH_TO_INCIDENT magnitude={record.magnitude}",
                )
            )
            return record
        raise RuntimeError("attach_report exceeded CAS retry budget")

    async def get_incident(self, incident_id: str) -> Optional[IncidentRecord]:
        doc = await self._find_doc(incident_id)
        return self._to_record(doc) if doc is not None else None

    async def get_open_incidents(
        self, intent_category: SignalCategory
    ) -> list[IncidentRecord]:
        docs = await self._query_partition(intent_category)
        return [
            self._to_record(d)
            for d in docs
            if d.get("status") == IncidentStatus.OPEN.value
        ]

    async def get_open_incident_vectors(
        self, intent_category: SignalCategory
    ) -> list[tuple[str, list[float]]]:
        docs = await self._query_partition(intent_category)
        return [
            (d["id"], list(d.get("embedding", [])))
            for d in docs
            if d.get("status") == IncidentStatus.OPEN.value
        ]

    async def report_count(self, incident_id: str) -> int:
        """Number of attached reports (test/inspection helper)."""
        doc = await self._find_doc(incident_id)
        return len(doc.get("reports", [])) if doc is not None else 0

    # ------------------------------------------------------------------ #
    # Cosmos query helpers
    # ------------------------------------------------------------------ #
    async def _find_doc(self, incident_id: str) -> Optional[dict[str, Any]]:
        query = "SELECT * FROM c WHERE c.id = @id"
        params = [{"name": "@id", "value": incident_id}]
        async for doc in self._container.query_items(
            query=query, parameters=params, enable_cross_partition_query=True
        ):
            return doc
        return None

    async def _query_partition(
        self, intent_category: SignalCategory
    ) -> list[dict[str, Any]]:
        query = "SELECT * FROM c WHERE c.intent_category = @cat"
        params = [{"name": "@cat", "value": intent_category.value}]
        results: list[dict[str, Any]] = []
        async for doc in self._container.query_items(
            query=query, parameters=params, partition_key=intent_category.value
        ):
            results.append(doc)
        return results


def _precondition_failures() -> tuple[type[BaseException], ...]:
    """Exception types that signal a lost optimistic-concurrency (etag) race."""
    from azure.cosmos.exceptions import CosmosAccessConditionFailedError

    return (CosmosAccessConditionFailedError,)
