"""Verify live Azure model clients use nonblocking token acquisition."""

from __future__ import annotations

import asyncio
import time

import agent_framework.openai as maf_openai
import azure.identity.aio as azure_identity_aio
import pytest
from azure.core.credentials import AccessToken
from azure.core.credentials_async import AsyncTokenCredential

import app.services.azure.failover_chat_client as failover
from app.core import dependencies
from app.core.config import Settings


def test_live_model_factories_share_async_azure_credential(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    dependencies.clear_service_caches()
    settings = Settings(
        mock_mode=False,
        environment="development",
        azure_openai_endpoint="https://models.example.test/",
        azure_openai_api_key="",
        azure_openai_deployment="gpt-demo",
        azure_search_endpoint="https://search.example.test/",
        azure_search_key="test-search-key",
        cosmos_db_endpoint="https://cosmos.example.test:443/",
    )
    credential = object()
    received: list[object] = []
    monkeypatch.setattr(dependencies, "get_settings", lambda: settings)
    monkeypatch.setattr(
        azure_identity_aio,
        "DefaultAzureCredential",
        lambda: credential,
    )

    class FakeChatClient:
        def __init__(self, **kwargs: object) -> None:
            received.append(kwargs["credential"])

    class FakeEmbeddingClient:
        def __init__(self, **kwargs: object) -> None:
            received.append(kwargs["credential"])

    monkeypatch.setattr(maf_openai, "OpenAIChatClient", FakeChatClient)
    monkeypatch.setattr(maf_openai, "OpenAIEmbeddingClient", FakeEmbeddingClient)
    monkeypatch.setattr(failover, "build_failover_client", lambda clients, _names: clients[0])

    try:
        dependencies.get_chat_client()
        dependencies.get_embedding_fn()

        assert received == [credential, credential]
        assert dependencies.get_async_azure_credential() is credential
    finally:
        dependencies.clear_service_caches()


async def test_azure_async_token_provider_keeps_event_loop_responsive() -> None:
    class DelayedCredential(AsyncTokenCredential):
        def __init__(self) -> None:
            self.started = asyncio.Event()
            self.release = asyncio.Event()

        async def get_token(self, *scopes: str, **_kwargs: object) -> AccessToken:
            self.started.set()
            await self.release.wait()
            return AccessToken("nonsecret-test-token", int(time.time()) + 3600)

        async def close(self) -> None:
            return None

    from agent_framework.openai import OpenAIEmbeddingClient

    credential = DelayedCredential()
    client = OpenAIEmbeddingClient(
        model="text-embedding-3-small",
        azure_endpoint="https://models.example.test/",
        credential=credential,
    )
    assert asyncio.iscoroutinefunction(client.client._azure_ad_token_provider)
    ticks = 0
    finished = asyncio.Event()

    async def heartbeat() -> None:
        nonlocal ticks
        while not finished.is_set():
            ticks += 1
            await asyncio.sleep(0.001)

    token_task = asyncio.create_task(client.client._get_azure_ad_token())
    heartbeat_task = asyncio.create_task(heartbeat())
    try:
        await asyncio.wait_for(credential.started.wait(), timeout=1)
        await asyncio.sleep(0.01)
        assert ticks > 1
        credential.release.set()
        token = await token_task
    finally:
        credential.release.set()
        finished.set()
        await heartbeat_task
        await client.client.close()

    assert token == "nonsecret-test-token"
