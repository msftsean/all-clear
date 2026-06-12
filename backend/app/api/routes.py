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

from typing import Literal, Optional

from fastapi import APIRouter, Body, Depends, HTTPException, status

from app.agents.pipeline import AllClearPipeline
from app.agents.schemas import KnowledgeArticle, PipelineResult
from app.core.config import Settings, get_settings
from app.core.dependencies import get_knowledge_service, get_pipeline
from app.services.interfaces import KnowledgeServiceInterface

router = APIRouter()

DEMO_CLEARBOARD = {
    "mode": "loaded",
    "total_signals": 1240,
    "headline": "Surge: many Signals in → few Incidents out",
    "subhead": (
        "Every Signal is preserved as a Report; ClearBoard merges pins on dedup "
        "and raises Incident Magnitude."
    ),
    "incidents": [
        {
            "incident_id": "AC-1240",
            "title": "Downtown high-rise fire",
            "location": "3rd & Pine downtown",
            "queue": "Fire / EMS",
            "severity": "SEV1",
            "report_count": 812,
            "sla_minutes": 5,
            "dedup_similarity": 0.94,
            "status": "escalated",
            "summary": (
                "Smoke and visible flames reported from the same downtown tower; "
                "callers describe one shared fire scene."
            ),
            "sample_signals": [
                "I can see flames from the upper floors at 3rd and Pine.",
                "Smoke pouring out of the high-rise downtown near Pine.",
            ],
        },
        {
            "incident_id": "AC-1241",
            "title": "Eastside power outage",
            "location": "Eastside substation corridor",
            "queue": "Utilities",
            "severity": "SEV2",
            "report_count": 351,
            "sla_minutes": 15,
            "dedup_similarity": 0.91,
            "status": "crews dispatched",
            "summary": (
                "Neighborhood reports map to one eastside outage footprint around "
                "the same substation corridor."
            ),
            "sample_signals": [
                "The whole eastside block lost power ten minutes ago.",
                "Traffic lights are out along the eastside corridor.",
            ],
        },
        {
            "incident_id": "AC-1242",
            "title": "Gas leak on Oak St",
            "location": "Oak St & 7th Ave",
            "queue": "Hazmat",
            "severity": "SEV1",
            "report_count": 77,
            "sla_minutes": 5,
            "dedup_similarity": 0.89,
            "status": "evacuation advised",
            "summary": (
                "Reports of gas odor and hissing cluster at Oak Street and 7th Avenue."
            ),
            "sample_signals": [
                "Strong gas smell outside the laundromat on Oak Street.",
                "I hear hissing near the Oak and 7th construction trench.",
            ],
        },
    ],
}


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


@router.get("/demo/clearboard", tags=["Demo"], summary="Idempotent ClearBoard demo fixture")
async def demo_clearboard(mode: Literal["blank", "loaded"] = "loaded") -> dict:
    """Return the safe, idempotent live-demo board fixture.

    ``mode=blank`` intentionally returns zero signals/incidents for before/after
    contrast; ``mode=loaded`` returns the hero scenario without mutating live data.
    """
    if mode == "blank":
        return {
            "mode": "blank",
            "total_signals": 0,
            "headline": "The board is quiet.",
            "subhead": "Clean slate before the signal surge.",
            "incidents": [],
        }
    return DEMO_CLEARBOARD
