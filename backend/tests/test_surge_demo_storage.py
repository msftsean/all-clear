"""Opt-in in-memory persistence for the live Room Surge demo."""

from __future__ import annotations

from datetime import UTC, datetime
from types import SimpleNamespace

import pytest
from fastapi.testclient import TestClient

from app.agents.router_agent import RouterExecutor
from app.agents.schemas import (
    IncidentRecord,
    Queue,
    RoutingOutcome,
    Severity,
    SignalCategory,
    SignalClassification,
    SignalEntities,
)
from app.core import dependencies
from app.core.config import Settings, get_settings
from app.main import create_app


@pytest.fixture(autouse=True)
def clear_dependencies() -> None:
    dependencies.clear_service_caches()
    yield
    dependencies.clear_service_caches()


def _settings(**overrides: object) -> Settings:
    values: dict[str, object] = {
        "mock_mode": False,
        "environment": "development",
        "azure_openai_endpoint": "https://models.example.test/",
        "azure_openai_api_key": "test-key",
        "azure_openai_deployment": "gpt-demo",
        "azure_search_endpoint": "https://search.example.test/",
        "azure_search_key": "test-search-key",
        "cosmos_db_endpoint": "https://cosmos.example.test:443/",
    }
    values.update(overrides)
    return Settings(**values)


async def test_hybrid_mode_uses_memory_stores_and_live_azure_providers(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    settings = _settings(surge_demo_memory_storage=True)
    monkeypatch.setattr(dependencies, "get_settings", lambda: settings)

    from app.services.mock.incident_store import MockIncidentStore
    from app.services.mock.session_store import MockSessionStore

    assert isinstance(dependencies.get_incident_store(), MockIncidentStore)
    assert isinstance(dependencies.get_session_store(), MockSessionStore)

    import agent_framework.openai as maf_openai

    import app.services.azure.failover_chat_client as failover
    import app.services.azure.knowledge_service as azure_knowledge

    chat_calls: list[dict[str, object]] = []
    embedding_calls: list[dict[str, object]] = []
    class_calls: list[str] = []
    embedding_inputs: list[str] = []
    azure_vector = [0.125, -0.5, 0.75, 0.25]

    class FakeChatClient:
        def __init__(self, **kwargs: object) -> None:
            chat_calls.append(kwargs)

    class FakeEmbeddingClient:
        def __init__(self, **kwargs: object) -> None:
            embedding_calls.append(kwargs)

        async def get_embeddings(self, texts: list[str]) -> list[SimpleNamespace]:
            embedding_inputs.extend(texts)
            return [SimpleNamespace(vector=list(azure_vector)) for _ in texts]

    class FakeKnowledgeService:
        def __init__(self, **kwargs: object) -> None:
            class_calls.append("azure-knowledge")

    monkeypatch.setattr(maf_openai, "OpenAIChatClient", FakeChatClient)
    monkeypatch.setattr(maf_openai, "OpenAIEmbeddingClient", FakeEmbeddingClient)
    monkeypatch.setattr(failover, "build_failover_client", lambda clients, names: clients[0])
    monkeypatch.setattr(azure_knowledge, "AzureSearchKnowledgeService", FakeKnowledgeService)

    dependencies.get_chat_client()
    dependencies.get_embedding_fn()
    dependencies.get_knowledge_service()

    assert chat_calls and chat_calls[0]["model"] == "gpt-demo"
    assert chat_calls[0]["azure_endpoint"] == settings.azure_openai_endpoint
    assert embedding_calls and embedding_calls[0]["model"] == "text-embedding-3-small"
    assert class_calls == ["azure-knowledge"]

    async def exercise_real_vector_persistence() -> None:
        store = MockIncidentStore()
        embed = dependencies.get_embedding_fn()
        router = RouterExecutor(embed, store, settings)
        classification = SignalClassification(
            intent="report_field_hazard",
            intent_category=SignalCategory.FIELD_HAZARD,
            target_queue=Queue.FIELD_OPERATIONS,
            confidence=0.95,
            entities=SignalEntities(),
        )
        original = "Flooding by Clarendon station on Wilson Boulevard"
        paraphrase = "Water is running across Wilson Boulevard near Clarendon station"
        first, first_vector = await router.decide(original, classification)
        assert first.outcome is RoutingOutcome.OPEN_INCIDENT
        incident_id = await store.next_incident_id()
        await store.create_incident(
            IncidentRecord(
                incident_id=incident_id,
                queue=Queue.FIELD_OPERATIONS,
                severity=Severity.SEV2,
                summary="Water main issue",
                intent_category=SignalCategory.FIELD_HAZARD,
                sla_minutes=60,
                created_at=datetime.now(UTC),
            ),
            first_vector,
        )
        second, _ = await router.decide(paraphrase, classification)

        assert second.outcome is RoutingOutcome.ATTACH_TO_INCIDENT
        assert second.matched_incident_id == incident_id
        assert await store.get_open_incident_vectors(SignalCategory.FIELD_HAZARD) == [
            (incident_id, azure_vector)
        ]
        assert embedding_inputs == [original, paraphrase]

    await exercise_real_vector_persistence()


def test_live_mode_without_opt_in_keeps_cosmos_stores(monkeypatch: pytest.MonkeyPatch) -> None:
    settings = _settings()
    monkeypatch.setattr(dependencies, "get_settings", lambda: settings)

    import app.services.azure.incident_store as azure_incidents
    import app.services.azure.session_store as azure_sessions

    incident_marker = object()
    session_marker = object()
    incident_calls: list[Settings] = []
    session_calls: list[Settings] = []
    monkeypatch.setattr(
        azure_incidents.AzureCosmosIncidentStore,
        "from_settings",
        classmethod(lambda cls, received: incident_calls.append(received) or incident_marker),
    )
    monkeypatch.setattr(
        azure_sessions.AzureCosmosSessionStore,
        "from_settings",
        classmethod(lambda cls, received: session_calls.append(received) or session_marker),
    )

    assert dependencies.get_incident_store() is incident_marker
    assert dependencies.get_session_store() is session_marker
    assert incident_calls == [settings]
    assert session_calls == [settings]


def test_memory_demo_does_not_require_cosmos_but_keeps_live_service_requirements() -> None:
    hybrid = _settings(
        surge_demo_memory_storage=True,
        cosmos_db_endpoint="",
        azure_openai_endpoint="",
        azure_search_endpoint="",
    )
    ordinary_live = _settings(cosmos_db_endpoint="")

    assert hybrid.missing_live_settings() == [
        "AZURE_OPENAI_ENDPOINT",
        "AZURE_SEARCH_ENDPOINT",
    ]
    assert ordinary_live.missing_live_settings() == ["AZURE_COSMOS_ENDPOINT"]


def test_memory_storage_flag_is_opt_in_through_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("SURGE_DEMO_MEMORY_STORAGE", "true")
    assert (
        Settings(
            _env_file=None,
            mock_mode=False,
            environment="development",
        ).surge_demo_memory_storage
        is True
    )


@pytest.mark.parametrize(
    ("settings", "expected_mock", "expected_storage"),
    [
        (_settings(mock_mode=True), True, "memory"),
        (_settings(surge_demo_memory_storage=True), False, "memory"),
        (_settings(), False, "cosmos"),
    ],
)
def test_health_reports_ai_and_storage_modes_independently(
    settings: Settings,
    expected_mock: bool,
    expected_storage: str,
) -> None:
    client = TestClient(create_app())
    client.app.dependency_overrides[get_settings] = lambda: settings
    try:
        response = client.get("/api/health")
    finally:
        client.app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json()["mock_mode"] is expected_mock
    assert response.json()["storage_mode"] == expected_storage
    assert response.json()["status"] == "healthy"
