"""
Dependency injection container for the Front Door Support Agent.
Provides service instances based on configuration (mock vs production).
"""

from functools import lru_cache
from typing import Annotated

from fastapi import Depends

from app.core.config import Settings, get_settings
from app.services.interfaces import (
    AuditLogInterface,
    BrandingServiceInterface,
    KnowledgeServiceInterface,
    LLMServiceInterface,
    PhoneServiceInterface,
    RealtimeServiceInterface,
    SessionStoreInterface,
    TicketServiceInterface,
)


@lru_cache
def get_llm_service(settings: Settings | None = None) -> LLMServiceInterface:
    """Get LLM service instance (mock or production)."""
    if settings is None:
        settings = get_settings()

    if settings.use_mock_services:
        from app.services.mock.llm_service import MockLLMService
        return MockLLMService()
    else:
        from app.services.azure.llm_service import AzureOpenAILLMService
        # Pass API key only if explicitly set (for local dev), otherwise use managed identity
        api_key = settings.azure_openai_api_key if settings.azure_openai_api_key else None
        return AzureOpenAILLMService(
            endpoint=settings.azure_openai_endpoint,
            deployment=settings.azure_openai_deployment,
            api_version=settings.azure_openai_api_version,
            api_key=api_key,
        )


@lru_cache
def get_ticket_service(settings: Settings | None = None) -> TicketServiceInterface:
    """Get ticket service instance (mock or production)."""
    if settings is None:
        settings = get_settings()

    if settings.use_mock_services:
        from app.services.mock.ticket_service import MockTicketService
        return MockTicketService()
    else:
        # TODO: Implement ServiceNow service
        from app.services.mock.ticket_service import MockTicketService
        return MockTicketService()


@lru_cache
def get_knowledge_service(settings: Settings | None = None) -> KnowledgeServiceInterface:
    """Get knowledge service instance (mock or production)."""
    if settings is None:
        settings = get_settings()

    if settings.use_mock_services:
        from app.services.mock.knowledge_service import MockKnowledgeService
        return MockKnowledgeService()
    else:
        from app.services.azure.knowledge_service import AzureSearchKnowledgeService
        api_key = settings.azure_openai_api_key if settings.azure_openai_api_key else None
        return AzureSearchKnowledgeService(
            search_endpoint=settings.azure_search_endpoint,
            search_key=settings.azure_search_key,
            index_name=settings.azure_search_index,
            openai_endpoint=settings.azure_openai_endpoint,
            openai_api_key=api_key,
        )


@lru_cache
def get_session_store(settings: Settings | None = None) -> SessionStoreInterface:
    """Get session store instance (mock or production)."""
    if settings is None:
        settings = get_settings()

    if settings.use_mock_services:
        from app.services.mock.session_store import MockSessionStore
        return MockSessionStore()
    else:
        # TODO: Implement Cosmos DB session store
        from app.services.mock.session_store import MockSessionStore
        return MockSessionStore()


@lru_cache
def get_audit_log(settings: Settings | None = None) -> AuditLogInterface:
    """Get audit log instance (mock or production)."""
    if settings is None:
        settings = get_settings()

    if settings.use_mock_services:
        from app.services.mock.audit_log import MockAuditLog
        return MockAuditLog()
    else:
        # TODO: Implement Cosmos DB audit log
        from app.services.mock.audit_log import MockAuditLog
        return MockAuditLog()


@lru_cache
def get_branding_service(settings: Settings | None = None) -> BrandingServiceInterface:
    """Get branding service instance (mock or production)."""
    if settings is None:
        settings = get_settings()

    if settings.use_mock_services:
        from app.services.mock.branding_service import MockBrandingService
        return MockBrandingService()
    else:
        # TODO: Implement Cosmos DB branding service
        from app.services.mock.branding_service import MockBrandingService
        return MockBrandingService()


@lru_cache
def get_realtime_service(settings: Settings | None = None) -> RealtimeServiceInterface:
    """Get realtime service instance (mock or production)."""
    if settings is None:
        settings = get_settings()

    if settings.use_mock_services:
        from app.services.mock.realtime import MockRealtimeService
        return MockRealtimeService()
    else:
        from app.services.azure.realtime import AzureRealtimeService
        # Pass API key only if explicitly set (for local dev), otherwise use managed identity
        api_key = settings.azure_openai_api_key if settings.azure_openai_api_key else None
        return AzureRealtimeService(
            endpoint=settings.realtime_endpoint,
            deployment=settings.azure_openai_realtime_deployment,
            api_version=settings.azure_openai_realtime_api_version,
            api_key=api_key,
        )


@lru_cache
def get_phone_service(settings: Settings | None = None) -> PhoneServiceInterface:
    """Get phone service instance (mock or production)."""
    if settings is None:
        settings = get_settings()

    if settings.use_mock_services:
        from app.services.mock.phone import MockPhoneService
        return MockPhoneService()
    else:
        from app.services.azure.phone import AzurePhoneService
        # Use connection string if provided, otherwise fall back to managed identity
        connection_string = settings.azure_acs_connection_string if settings.azure_acs_connection_string else None
        return AzurePhoneService(
            acs_endpoint=settings.azure_acs_endpoint,
            openai_endpoint=settings.realtime_endpoint,
            openai_deployment=settings.azure_openai_realtime_deployment,
            connection_string=connection_string,
        )


# FastAPI dependency annotations
SettingsDep = Annotated[Settings, Depends(get_settings)]
LLMServiceDep = Annotated[LLMServiceInterface, Depends(get_llm_service)]
TicketServiceDep = Annotated[TicketServiceInterface, Depends(get_ticket_service)]
KnowledgeServiceDep = Annotated[KnowledgeServiceInterface, Depends(get_knowledge_service)]
SessionStoreDep = Annotated[SessionStoreInterface, Depends(get_session_store)]
AuditLogDep = Annotated[AuditLogInterface, Depends(get_audit_log)]
BrandingServiceDep = Annotated[BrandingServiceInterface, Depends(get_branding_service)]
RealtimeServiceDep = Annotated[RealtimeServiceInterface, Depends(get_realtime_service)]
PhoneServiceDep = Annotated[PhoneServiceInterface, Depends(get_phone_service)]


def clear_service_caches() -> None:
    """Clear all cached service instances (for testing)."""
    get_llm_service.cache_clear()
    get_ticket_service.cache_clear()
    get_knowledge_service.cache_clear()
    get_session_store.cache_clear()
    get_audit_log.cache_clear()
    get_branding_service.cache_clear()
    get_realtime_service.cache_clear()
    get_phone_service.cache_clear()
    get_chat_client.cache_clear()
    get_embedding_fn.cache_clear()
    get_incident_store.cache_clear()
    get_pipeline.cache_clear()


# =============================================================================
# All Clear: MAF pipeline factories (001-maf-rehost, T10)
#
# Mock vs live client factories for the three-agent incident pipeline. The mock
# path (USE_MOCK_MODE/use_mock_services=true) is fully offline; the live path
# reaches Azure OpenAI via OpenAIChatClient with azure_endpoint (plan.md App. B:
# there is NO AzureOpenAIChatClient). All live imports are lazy so mock mode
# never requires Azure packages or credentials (Constitution Art. V).
# =============================================================================


@lru_cache
def get_chat_client():  # type: ignore[no-untyped-def]
    """Return the MAF chat client: MockChatClient (mock) or Azure OpenAI (live)."""
    settings = get_settings()

    if settings.use_mock_services:
        from app.services.mock.maf_chat_client import MockChatClient

        return MockChatClient()

    from agent_framework.openai import OpenAIChatClient

    # The gpt-5.1 Responses API surface (/openai/v1/) accepts only api-version
    # "preview"; dated versions return 400 (001-maf-rehost T13). Force it here so
    # the chat client is correct regardless of the configured default.
    chat_api_version = "preview"

    api_key = settings.azure_openai_api_key or None
    if api_key:
        return OpenAIChatClient(
            model=settings.azure_openai_deployment,
            azure_endpoint=settings.azure_openai_endpoint,
            api_version=chat_api_version,
            api_key=api_key,
        )
    from azure.identity import DefaultAzureCredential

    return OpenAIChatClient(
        model=settings.azure_openai_deployment,
        azure_endpoint=settings.azure_openai_endpoint,
        api_version=chat_api_version,
        credential=DefaultAzureCredential(),
    )


@lru_cache
def get_embedding_fn():  # type: ignore[no-untyped-def]
    """Return an async EmbeddingFn: deterministic mock embeddings or Azure OpenAI."""
    settings = get_settings()

    if settings.use_mock_services:
        from app.services.mock.embeddings import mock_embed

        return mock_embed

    from agent_framework.openai import OpenAIEmbeddingClient

    # The embeddings surface (/deployments/{model}/embeddings) needs a dated GA
    # api-version (e.g. 2024-10-21); "preview" returns 404 DeploymentNotFound
    # (001-maf-rehost T13). This is deliberately independent of the chat client's
    # "preview" version — the two surfaces accept different versions.
    embed_api_version = "2024-10-21"

    api_key = settings.azure_openai_api_key or None
    model = getattr(settings, "azure_openai_embedding_deployment", None) or "text-embedding-3-small"
    if api_key:
        client = OpenAIEmbeddingClient(
            model=model,
            azure_endpoint=settings.azure_openai_endpoint,
            api_version=embed_api_version,
            api_key=api_key,
        )
    else:
        from azure.identity import DefaultAzureCredential

        client = OpenAIEmbeddingClient(
            model=model,
            azure_endpoint=settings.azure_openai_endpoint,
            api_version=embed_api_version,
            credential=DefaultAzureCredential(),
        )

    async def _embed(text: str) -> list[float]:
        from app.agents.retry import with_rate_limit_retry

        response = await with_rate_limit_retry(
            lambda: client.get_embeddings([text])
        )
        return list(response[0].vector) if response else []

    return _embed


@lru_cache
def get_incident_store():  # type: ignore[no-untyped-def]
    """Return the incident store. Cached so dedup state persists across requests.

    Mock mode uses the in-memory MockIncidentStore; live mode uses the durable
    Cosmos `incidents` store (spec 016 D1/D2). Live imports are lazy so mock mode
    never requires the Cosmos SDK or credentials (Constitution Art. V).
    """
    settings = get_settings()

    if settings.use_mock_services:
        from app.services.mock.incident_store import MockIncidentStore

        return MockIncidentStore()

    from app.services.azure.incident_store import AzureCosmosIncidentStore

    return AzureCosmosIncidentStore.from_settings(settings)


@lru_cache
def get_pipeline():  # type: ignore[no-untyped-def]
    """Build the AllClearPipeline wired for the current mode (mock or live)."""
    settings = get_settings()

    from app.agents.action_agent import ActionExecutor, ActionToolbox
    from app.agents.pipeline import AllClearPipeline
    from app.agents.query_agent import build_query_agent
    from app.agents.router_agent import RouterExecutor

    client = get_chat_client()
    embed = get_embedding_fn()
    store = get_incident_store()
    knowledge = get_knowledge_service()

    query_agent = build_query_agent(client)
    router = RouterExecutor(embed, store, settings)
    toolbox = ActionToolbox(store, knowledge, embed, settings)
    action = ActionExecutor(toolbox, store)
    return AllClearPipeline(query_agent, router, action, store=store)
