"""Focused tests for live Azure Search vector-query construction and safe timings."""

from __future__ import annotations

import pytest

import app.services.azure.knowledge_service as knowledge_module
from app.services.azure.knowledge_service import AzureSearchKnowledgeService


async def test_vector_query_uses_supported_k_and_logs_no_signal_text(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    search_calls: list[dict] = []

    class FakeSearchClient:
        def search(self, **kwargs: object) -> list[dict]:
            search_calls.append(kwargs)
            return []

    async def inline_to_thread(function, *args, **kwargs):
        return function(*args, **kwargs)

    service = AzureSearchKnowledgeService.__new__(AzureSearchKnowledgeService)
    service._search_client = FakeSearchClient()
    service._get_embedding = lambda _text: [0.1, 0.2, 0.3]
    monkeypatch.setattr(knowledge_module.asyncio, "to_thread", inline_to_thread)
    signal_text = "private signal wording that must not appear in logs"

    await service.search_with_content(signal_text, limit=4)

    vector_query = search_calls[0]["vector_queries"][0]
    assert vector_query.k == 12
    assert vector_query.fields == "content_vector"
    output = capsys.readouterr().out
    assert "azure_search_phases" in output
    assert "vector_query=True" in output
    assert signal_text not in output
