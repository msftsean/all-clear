"""
Live smoke test for the All Clear pipeline (001-maf-rehost, T13).

RESERVED FOR SEAN. This runs one inbound signal end-to-end against a *live* Azure
OpenAI deployment (no mock client), to validate the gpt-5.1 -> gpt-4.1 fallback chain
and observe quota behavior. The mock suite (USE_MOCK_MODE=true pytest) already proves
correctness; this proves the live wiring and model behavior.

Usage (from backend/):
    python scripts/live_smoke.py --deployment gpt-5.1
    python scripts/live_smoke.py --deployment gpt-4.1

Auth: uses the Azure OpenAI api key if AZURE_OPENAI_API_KEY is set, otherwise
DefaultAzureCredential (managed identity / az login). Endpoint and api-version come
from settings (.env / environment). Per plan.md Appendix B there is NO
AzureOpenAIChatClient — the live client is OpenAIChatClient with azure_endpoint.
"""

from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path

_BACKEND = Path(__file__).resolve().parents[1]
if str(_BACKEND) not in sys.path:
    sys.path.insert(0, str(_BACKEND))

from app.agents.action_agent import ActionExecutor, ActionToolbox  # noqa: E402
from app.agents.pipeline import AllClearPipeline  # noqa: E402
from app.agents.query_agent import build_query_agent  # noqa: E402
from app.agents.router_agent import RouterExecutor  # noqa: E402
from app.core.config import get_settings  # noqa: E402
from app.services.mock.incident_store import MockIncidentStore  # noqa: E402
from app.services.mock.knowledge_service import MockKnowledgeService  # noqa: E402

DEFAULT_SIGNAL = (
    "There's a downed power line sparking across the road at 5th and Main, "
    "traffic is backing up and it looks dangerous."
)


def _build_live_pipeline(deployment: str) -> AllClearPipeline:
    """Construct a pipeline backed by a live Azure OpenAI deployment."""
    settings = get_settings()
    if not settings.azure_openai_endpoint:
        raise SystemExit(
            "AZURE_OPENAI_ENDPOINT is not set. Configure .env/environment before live smoke."
        )

    from agent_framework.openai import OpenAIChatClient, OpenAIEmbeddingClient

    api_key = settings.azure_openai_api_key or None
    if api_key:
        auth = {"api_key": api_key}
    else:
        from azure.identity import DefaultAzureCredential

        auth = {"credential": DefaultAzureCredential()}

    endpoint = settings.azure_openai_endpoint

    # Azure routes the two clients through different surfaces, each with its own
    # accepted api-version (verified against this resource):
    #   * Chat uses the Responses API on the GA /openai/v1/ surface, which accepts
    #     only api-version="preview" (dated versions return "API version not supported").
    #   * Embeddings use the classic /deployments/{model}/embeddings path, which
    #     accepts dated GA versions (e.g. 2024-10-21). Preview-dated versions return
    #     DeploymentNotFound here, so we pin a verified GA version.
    chat_api_version = "preview"
    embed_api_version = "2024-10-21"

    chat_client = OpenAIChatClient(
        model=deployment,
        azure_endpoint=endpoint,
        api_version=chat_api_version,
        **auth,
    )

    embed_model = getattr(
        settings, "azure_openai_embedding_deployment", None
    ) or "text-embedding-3-small"
    embed_client = OpenAIEmbeddingClient(
        model=embed_model,
        azure_endpoint=endpoint,
        api_version=embed_api_version,
        **auth,
    )

    async def embed(text: str) -> list[float]:
        response = await embed_client.get_embeddings([text])
        return list(response[0].vector) if response else []

    store = MockIncidentStore()
    knowledge = MockKnowledgeService()
    query_agent = build_query_agent(chat_client)
    router = RouterExecutor(embed, store, settings)
    toolbox = ActionToolbox(store, knowledge, embed, settings)
    action = ActionExecutor(toolbox, store)
    return AllClearPipeline(query_agent, router, action, store=store, bus=None)


async def _run(deployment: str, signal: str) -> int:
    pipeline = _build_live_pipeline(deployment)
    print(f"== Live smoke :: deployment={deployment} ==")
    print(f"signal: {signal}\n")
    result = await pipeline.process_signal(text=signal, session_id="live-smoke", channel="chat")
    print(f"intent_category : {result.classification.intent_category.value}")
    print(f"confidence      : {result.classification.confidence:.2f}")
    print(f"outcome         : {result.routing.outcome.value}")
    print(f"severity        : {result.routing.severity.value} (SLA {result.routing.sla_minutes}m)")
    print(f"queue           : {result.routing.target_queue.value}")
    print(f"escalate        : {result.routing.escalate} ({result.routing.escalation_reason})")
    print(f"incident_id     : {result.action.incident_id}")
    print(f"action status   : {result.action.status.value}")
    print(f"processing_ms   : {result.processing_ms}")
    print(f"user_message    : {result.action.user_message}")
    print(f"\nsignal_text (stored/returned, redacted): {result.signal_text}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="All Clear live smoke test (T13).")
    parser.add_argument(
        "--deployment", required=True, help="Azure OpenAI deployment, e.g. gpt-5.1 or gpt-4.1"
    )
    parser.add_argument(
        "--signal", default=DEFAULT_SIGNAL, help="Inbound signal text to run end-to-end"
    )
    args = parser.parse_args()
    return asyncio.run(_run(args.deployment, args.signal))


if __name__ == "__main__":
    raise SystemExit(main())
