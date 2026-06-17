"""
Tests for conversation persistence (019-conversation-persistence).

Covers:
  1. AzureCosmosSessionStore CRUD operations against an in-memory fake container
  2. Session history API endpoints (GET /api/sessions/{id}, GET /api/sessions)
  3. Pipeline session persistence via process_signal with student_id_hash
  4. MockSessionStore lockstep (same scenarios run on both implementations)
"""

from __future__ import annotations

import hashlib
import uuid
from datetime import datetime, timezone
from typing import Any, AsyncIterator, Optional

import pytest
from fastapi.testclient import TestClient

from app.models.schemas import ConversationTurn, Session
from app.services.azure.session_store import AzureCosmosSessionStore
from app.services.interfaces import SessionStoreInterface
from app.services.mock.session_store import MockSessionStore


# =============================================================================
# In-memory Cosmos container fake
# =============================================================================


class FakeSessionContainer:
    """Minimal async stand-in for a Cosmos ContainerProxy (sessions container)."""

    def __init__(self) -> None:
        # keyed by (student_id_hash, session_id) -> document
        self._items: dict[tuple[str, str], dict[str, Any]] = {}

    @staticmethod
    def _partition(doc: dict[str, Any]) -> str:
        return str(doc["student_id_hash"])

    def _key(self, doc: dict[str, Any]) -> tuple[str, str]:
        return (self._partition(doc), doc["id"])

    async def create_item(self, body: dict[str, Any]) -> dict[str, Any]:
        stored = dict(body)
        self._items[self._key(stored)] = stored
        return stored

    async def replace_item(self, item: str, body: dict[str, Any]) -> dict[str, Any]:
        stored = dict(body)
        # find key by id
        for k in list(self._items.keys()):
            if k[1] == item:
                del self._items[k]
                break
        self._items[self._key(stored)] = stored
        return stored

    async def query_items(
        self,
        query: str,
        parameters: Optional[list[dict[str, Any]]] = None,
        partition_key: Optional[str] = None,
        enable_cross_partition_query: bool = False,
    ) -> AsyncIterator[dict[str, Any]]:
        """Minimal query engine: supports @sid and @hash parameter matching."""
        param_map = {p["name"]: p["value"] for p in (parameters or [])}

        results: list[dict[str, Any]] = []
        for doc in self._items.values():
            match = True
            if "@sid" in param_map and str(doc.get("session_id")) != param_map["@sid"]:
                match = False
            if "@hash" in param_map and doc.get("student_id_hash") != param_map["@hash"]:
                match = False
            if match:
                results.append(doc)

        # Respect ORDER BY last_active DESC if present
        if "ORDER BY" in query:
            results.sort(key=lambda d: d.get("last_active", ""), reverse=True)

        # Respect LIMIT
        if "LIMIT" in query:
            import re
            m = re.search(r"LIMIT (\d+)", query)
            if m:
                results = results[: int(m.group(1))]

        for r in results:
            yield r

    async def read(self) -> dict[str, Any]:
        return {"id": "sessions"}


# =============================================================================
# Shared fixture helpers
# =============================================================================


def _hash(val: str) -> str:
    return hashlib.sha256(val.encode()).hexdigest()


def _make_session(student_hash: Optional[str] = None) -> Session:
    now = datetime.now(timezone.utc)
    return Session(
        session_id=uuid.uuid4(),
        student_id_hash=student_hash or _hash("test-student"),
        created_at=now,
        last_active=now,
    )


# =============================================================================
# Parametrize over both store implementations
# =============================================================================


@pytest.fixture(params=["mock", "cosmos"])
def session_store(request: pytest.FixtureRequest) -> SessionStoreInterface:
    if request.param == "mock":
        store = MockSessionStore()
        MockSessionStore.clear_all()
        return store
    container = FakeSessionContainer()
    return AzureCosmosSessionStore(container)


# =============================================================================
# CRUD tests (run on both implementations)
# =============================================================================


@pytest.mark.asyncio
async def test_create_and_get_session(session_store: SessionStoreInterface) -> None:
    session = _make_session()
    await session_store.create_session(session)

    fetched = await session_store.get_session(session.session_id)
    assert fetched is not None
    assert fetched.session_id == session.session_id
    assert fetched.student_id_hash == session.student_id_hash


@pytest.mark.asyncio
async def test_get_nonexistent_session_returns_none(session_store: SessionStoreInterface) -> None:
    result = await session_store.get_session(uuid.uuid4())
    assert result is None


@pytest.mark.asyncio
async def test_update_session(session_store: SessionStoreInterface) -> None:
    session = _make_session()
    await session_store.create_session(session)

    session.topic_summary = "Financial Aid inquiry"
    session.incident_ids = ["AC-001"]
    await session_store.update_session(session)

    fetched = await session_store.get_session(session.session_id)
    assert fetched is not None
    assert fetched.topic_summary == "Financial Aid inquiry"
    assert "AC-001" in fetched.incident_ids


@pytest.mark.asyncio
async def test_conversation_turns_persisted(session_store: SessionStoreInterface) -> None:
    session = _make_session()
    now = datetime.now(timezone.utc)
    session.conversation_history.append(
        ConversationTurn(
            turn_number=1,
            timestamp=now,
            intent="infrastructure_failure",
            signal_text="Downtown building fire at 3rd and Pine",
            agent_response="Incident opened: AC-101. Crews dispatched.",
            incident_id="AC-101",
            input_modality="text",
        )
    )
    await session_store.create_session(session)

    fetched = await session_store.get_session(session.session_id)
    assert fetched is not None
    assert len(fetched.conversation_history) == 1
    turn = fetched.conversation_history[0]
    assert turn.signal_text == "Downtown building fire at 3rd and Pine"
    assert turn.incident_id == "AC-101"
    assert turn.input_modality == "text"


@pytest.mark.asyncio
async def test_get_sessions_by_student(session_store: SessionStoreInterface) -> None:
    student_hash = _hash("student-abc")
    other_hash = _hash("other-student")

    s1 = _make_session(student_hash)
    s2 = _make_session(student_hash)
    s3 = _make_session(other_hash)

    await session_store.create_session(s1)
    await session_store.create_session(s2)
    await session_store.create_session(s3)

    results = await session_store.get_sessions_by_student(student_hash, limit=10)
    ids = {str(s.session_id) for s in results}
    assert str(s1.session_id) in ids
    assert str(s2.session_id) in ids
    assert str(s3.session_id) not in ids


@pytest.mark.asyncio
async def test_get_sessions_by_student_respects_limit(session_store: SessionStoreInterface) -> None:
    student_hash = _hash("student-limit")
    for _ in range(5):
        s = _make_session(student_hash)
        await session_store.create_session(s)

    results = await session_store.get_sessions_by_student(student_hash, limit=3)
    assert len(results) <= 3


# =============================================================================
# AzureCosmosSessionStore: health check
# =============================================================================


@pytest.mark.asyncio
async def test_cosmos_health_check() -> None:
    container = FakeSessionContainer()
    store = AzureCosmosSessionStore(container)
    healthy, latency_ms, error = await store.health_check()
    assert healthy is True
    assert error is None


# =============================================================================
# Session history API endpoints
# =============================================================================


@pytest.fixture()
def api_client() -> TestClient:
    """TestClient wired to use MockSessionStore (cleared per test)."""
    from app.core.dependencies import clear_service_caches, get_session_store
    from app.main import create_app
    from app.services.mock.session_store import MockSessionStore

    MockSessionStore.clear_all()
    clear_service_caches()

    test_app = create_app()
    return TestClient(test_app)


def test_get_session_not_found(api_client: TestClient) -> None:
    missing_id = str(uuid.uuid4())
    resp = api_client.get(f"/api/sessions/{missing_id}")
    assert resp.status_code == 404


def test_list_sessions_missing_hash(api_client: TestClient) -> None:
    resp = api_client.get("/api/sessions")
    assert resp.status_code == 422  # missing required query param


def test_list_sessions_empty(api_client: TestClient) -> None:
    student_hash = _hash("nobody")
    resp = api_client.get(f"/api/sessions?student_id_hash={student_hash}")
    assert resp.status_code == 200
    assert resp.json() == []


def test_get_session_roundtrip(api_client: TestClient) -> None:
    """Create a session via MockSessionStore, retrieve it via the API."""
    from app.core.dependencies import get_session_store

    store = get_session_store()
    session = _make_session()

    import asyncio
    asyncio.run(store.create_session(session))

    resp = api_client.get(f"/api/sessions/{session.session_id}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["session_id"] == str(session.session_id)
    assert data["student_id_hash"] == session.student_id_hash


def test_list_sessions_returns_correct_student(api_client: TestClient) -> None:
    from app.core.dependencies import get_session_store

    store = get_session_store()
    student_hash = _hash("test-list-student")
    s1 = _make_session(student_hash)
    s2 = _make_session(student_hash)
    other = _make_session(_hash("other"))

    import asyncio
    asyncio.run(store.create_session(s1))
    asyncio.run(store.create_session(s2))
    asyncio.run(store.create_session(other))

    resp = api_client.get(f"/api/sessions?student_id_hash={student_hash}")
    assert resp.status_code == 200
    data = resp.json()
    returned_ids = {d["session_id"] for d in data}
    assert str(s1.session_id) in returned_ids
    assert str(s2.session_id) in returned_ids
    assert str(other.session_id) not in returned_ids


# =============================================================================
# Pipeline session persistence integration test
# =============================================================================


@pytest.mark.asyncio
async def test_pipeline_persists_turn_when_student_hash_provided() -> None:
    """process_signal with student_id_hash writes a ConversationTurn to store."""
    from app.agents.pipeline import build_mock_pipeline
    from app.services.mock.session_store import MockSessionStore

    MockSessionStore.clear_all()
    store = MockSessionStore()
    pipeline = build_mock_pipeline()
    pipeline.session_store = store

    student_hash = _hash("pipeline-test-student")
    session_id = str(uuid.uuid4())

    result = await pipeline.process_signal(
        text="Fire reported at Oak and 5th",
        session_id=session_id,
        channel="text",
        student_id_hash=student_hash,
    )

    sessions = await store.get_sessions_by_student(student_hash, limit=5)
    assert len(sessions) == 1
    assert len(sessions[0].conversation_history) == 1
    turn = sessions[0].conversation_history[0]
    assert turn.turn_number == 1
    assert turn.input_modality == "text"
    assert turn.signal_text is not None


@pytest.mark.asyncio
async def test_pipeline_no_persist_without_student_hash() -> None:
    """process_signal without student_id_hash leaves session store empty."""
    from app.agents.pipeline import build_mock_pipeline
    from app.services.mock.session_store import MockSessionStore

    MockSessionStore.clear_all()
    store = MockSessionStore()
    pipeline = build_mock_pipeline()
    pipeline.session_store = store

    await pipeline.process_signal(
        text="Gas leak at 7th and Elm",
        session_id="anon-session",
        channel="text",
        student_id_hash=None,
    )

    # No student hash → no session created
    assert MockSessionStore._sessions == {}


@pytest.mark.asyncio
async def test_pipeline_accumulates_turns_across_calls() -> None:
    """Multiple calls with the same student_id_hash append turns to the same session."""
    from app.agents.pipeline import build_mock_pipeline
    from app.services.mock.session_store import MockSessionStore

    MockSessionStore.clear_all()
    store = MockSessionStore()
    pipeline = build_mock_pipeline()
    pipeline.session_store = store

    student_hash = _hash("multi-turn-student")
    session_id = str(uuid.uuid4())

    await pipeline.process_signal(
        text="Power outage on Eastside",
        session_id=session_id,
        student_id_hash=student_hash,
    )
    await pipeline.process_signal(
        text="Still no power after 2 hours",
        session_id=session_id,
        student_id_hash=student_hash,
    )

    sessions = await store.get_sessions_by_student(student_hash, limit=5)
    assert len(sessions) == 1
    # Both turns should be stored in the same session
    assert len(sessions[0].conversation_history) == 2
