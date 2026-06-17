"""
Azure Cosmos DB session store (spec 019-conversation-persistence).

Live twin of MockSessionStore. Persists conversation sessions in a Cosmos DB
for NoSQL container partitioned by ``/student_id_hash`` so all sessions for a
student land in the same logical partition for efficient list queries.

Bounded authority (Constitution Art. II): persistence only. No routing,
intent detection, or PII filtering — those happen upstream before this store
is called. Constitution Art. III: raw audio is never stored; only PII-safe
(already-redacted) text reaches here.

Uses ``AzureCosmosSessionStore.from_settings`` for the live, credentialed
instance; unit tests can inject an in-memory fake container.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Optional
from uuid import UUID

from app.models.schemas import Session
from app.services.interfaces import SessionStoreInterface


class AzureCosmosSessionStore(SessionStoreInterface):
    """SessionStore backed by an Azure Cosmos DB for NoSQL container.

    Args:
        container: An async Cosmos ``ContainerProxy`` (or an in-memory fake with
            the same surface) for the ``sessions`` container, partitioned on
            ``/student_id_hash``.
    """

    def __init__(self, container: Any) -> None:
        self._container = container

    # ------------------------------------------------------------------ #
    # Live factory
    # ------------------------------------------------------------------ #
    @classmethod
    def from_settings(cls, settings: Any) -> "AzureCosmosSessionStore":
        """Build a live, credentialed store from application settings.

        Uses the account key when configured; otherwise falls back to managed
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
        container_name = getattr(settings, "cosmos_db_sessions_container", "sessions")
        container = database.get_container_client(container_name)
        return cls(container)

    # ------------------------------------------------------------------ #
    # Serialization helpers
    # ------------------------------------------------------------------ #
    @staticmethod
    def _to_document(session: Session) -> dict[str, Any]:
        """Serialize a Session to a Cosmos document."""
        doc = session.model_dump(mode="json")
        doc["id"] = str(session.session_id)
        # Cosmos partition key is /student_id_hash; already in doc from model_dump
        return doc

    @staticmethod
    def _from_document(doc: dict[str, Any]) -> Session:
        """Deserialize a Cosmos document to a Session."""
        clean = {k: v for k, v in doc.items() if not k.startswith("_")}
        clean.pop("id", None)
        return Session.model_validate(clean)

    # ------------------------------------------------------------------ #
    # SessionStoreInterface implementation
    # ------------------------------------------------------------------ #
    async def create_session(self, session: Session) -> None:
        """Persist a new session document."""
        doc = self._to_document(session)
        await self._container.create_item(body=doc)

    async def get_session(self, session_id: UUID) -> Optional[Session]:
        """Retrieve a session by ID.

        Cosmos requires the partition key for a point-read. Since sessions are
        partitioned by student_id_hash and we only have session_id here, we fall
        back to a cross-partition query (acceptable for single-document lookup;
        no hot-partition risk for the point-read path).
        """
        try:
            query = "SELECT * FROM c WHERE c.session_id = @sid"
            params: list[dict[str, Any]] = [{"name": "@sid", "value": str(session_id)}]
            results = []
            async for item in self._container.query_items(
                query=query,
                parameters=params,
                enable_cross_partition_query=True,
            ):
                results.append(item)
            if not results:
                return None
            return self._from_document(results[0])
        except Exception:  # noqa: BLE001
            return None

    async def update_session(self, session: Session) -> None:
        """Replace an existing session document (last-write-wins)."""
        doc = self._to_document(session)
        await self._container.replace_item(
            item=str(session.session_id),
            body=doc,
        )

    async def get_sessions_by_student(
        self,
        student_id_hash: str,
        limit: int = 10,
    ) -> list[Session]:
        """Return up to ``limit`` sessions for a student, newest first."""
        query = (
            "SELECT * FROM c WHERE c.student_id_hash = @hash "
            "ORDER BY c.last_active DESC "
            f"OFFSET 0 LIMIT {max(1, min(limit, 100))}"
        )
        params: list[dict[str, Any]] = [{"name": "@hash", "value": student_id_hash}]
        sessions: list[Session] = []
        async for item in self._container.query_items(
            query=query,
            parameters=params,
            partition_key=student_id_hash,
        ):
            sessions.append(self._from_document(item))
        return sessions

    async def health_check(self) -> tuple[bool, Optional[int], Optional[str]]:
        """Ping the container; return (healthy, latency_ms, error_message)."""
        import time

        try:
            t0 = time.monotonic()
            await self._container.read()
            latency_ms = int((time.monotonic() - t0) * 1000)
            return True, latency_ms, None
        except Exception as exc:  # noqa: BLE001
            return False, None, str(exc)
