"""
All Clear signal API (001-maf-rehost, T10).

Replaces the retired FERPA ticket/department chat API with the incident-triage
contract. A single endpoint runs an inbound signal through the three-agent MAF
pipeline (QueryAgent -> RouterExecutor -> ActionExecutor) and returns the typed
``PipelineResult``. SSE lifecycle events are published onto the transcript bus by
the pipeline so the ClearBoard updates live.

The pipeline (mock vs live client) is provided by ``get_pipeline`` so this module is
free of any direct model/client wiring (Constitution Art. V).
"""

from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Body, Depends, HTTPException, status

from app.agents.pipeline import AllClearPipeline
from app.agents.schemas import KnowledgeArticle, PipelineResult
from app.core.config import Settings, get_settings
from app.core.dependencies import get_knowledge_service, get_pipeline
from app.services.interfaces import KnowledgeServiceInterface

router = APIRouter()


def _is_content_safety_block(exc: BaseException) -> bool:
    """True if ``exc`` (or anything in its cause/context chain) is an Azure
    OpenAI content-filter / Prompt Shield rejection.

    Robust against an upstream agent_framework defect: when Azure returns the
    inner-error code ``ContentFiltered`` (Prompt Shield / jailbreak detection),
    ``OpenAIContentFilterException.__init__`` raises ``ValueError`` while building
    its ``ContentFilterCodes`` enum, so a bare ``ValueError`` propagates instead
    of the typed exception. We therefore walk the whole chain and match on either
    the typed exception, an OpenAI ``content_filter`` BadRequestError, or the
    tell-tale enum-construction message.
    """
    seen: set[int] = set()
    cur: BaseException | None = exc
    while cur is not None and id(cur) not in seen:
        seen.add(id(cur))
        name = type(cur).__name__
        if "ContentFilter" in name:
            return True
        code = getattr(cur, "code", None)
        if code == "content_filter":
            return True
        text = str(cur)
        if "ContentFiltered" in text or "content management policy" in text.lower():
            return True
        cur = cur.__cause__ or cur.__context__
    return False


@router.post(
    "/chat",
    response_model=PipelineResult,
    tags=["Signals"],
    summary="Submit an inbound signal",
    description=(
        "Process an inbound signal through the three-agent incident pipeline: "
        "QueryAgent classifies, RouterExecutor deduplicates and maps severity/SLA, "
        "and ActionAgent opens or attaches the incident."
    ),
)
@router.post("/signals", response_model=PipelineResult, tags=["Signals"])
async def submit_signal(
    *,
    message: str = Body(..., embed=True, min_length=1, max_length=4000),
    session_id: Optional[str] = Body(default=None, embed=True),
    channel: str = Body(default="chat", embed=True),
    pipeline: AllClearPipeline = Depends(get_pipeline),
) -> PipelineResult:
    """Run a signal end-to-end and return the typed PipelineResult."""
    try:
        return await pipeline.process_signal(
            text=message,
            session_id=session_id or "anonymous",
            channel=channel,
        )
    except Exception as exc:  # noqa: BLE001 - translate model safety blocks to 4xx
        if _is_content_safety_block(exc):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    "Signal rejected by content safety policy and was not processed. "
                    "Rephrase without disallowed content."
                ),
            ) from exc
        raise


@router.get(
    "/knowledge/search",
    response_model=list[KnowledgeArticle],
    tags=["Knowledge"],
    summary="Search the knowledge base",
)
async def search_knowledge(
    query: str,
    limit: int = 3,
    knowledge_service: KnowledgeServiceInterface = Depends(get_knowledge_service),
) -> list[KnowledgeArticle]:
    """Search the knowledge base (incident-agnostic helper)."""
    results = await knowledge_service.search(query=query, department=None, limit=limit)
    return [
        KnowledgeArticle(
            article_id=a.article_id,
            title=a.title,
            url=a.url,
            snippet=a.snippet,
            relevance_score=a.relevance_score,
        )
        for a in results
    ]


@router.get("/health", tags=["Health"], summary="Service health")
async def health_check(settings: Settings = Depends(get_settings)) -> dict:
    """Lightweight health probe reporting the active mode."""
    return {
        "status": "healthy",
        "mock_mode": settings.use_mock_services,
        "domain": "all-clear-incident-triage",
    }
