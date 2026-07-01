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

from fastapi import APIRouter, Body, Depends, HTTPException, Response, status
from pydantic import BaseModel, Field

from app.agents.pipeline import AllClearPipeline
from app.agents.schemas import KnowledgeArticle, PipelineResult
from app.core.config import Settings, get_settings
from app.core.dependencies import (
    get_capstone_lead_store,
    get_knowledge_service,
    get_loadtest_coordinator,
    get_model_status,
    get_pipeline,
)
from app.services.scenario_packs import (
    clearboard_for_pack,
    dedup_probe_signals,
    list_available_packs,
)
from app.services.interfaces import KnowledgeServiceInterface

router = APIRouter()


class CapstoneLeadCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=120)
    agency: str = Field(..., min_length=1, max_length=160)
    surge: str = Field(..., min_length=1, max_length=500)
    signal_flood: str = Field(..., min_length=1, max_length=500)
    incident_underneath: str = Field(..., min_length=1, max_length=500)


def _require_capstone_demo_access(settings: Settings) -> None:
    """Capstone lead capture is demo-only and never exposed in live mode."""
    if not settings.use_mock_services:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Capstone lead capture is disabled outside mock mode.",
        )


AZURE_FOOTPRINT_SERVICES = [
    ("azure_openai", "Azure OpenAI"),
    ("embeddings", "Embeddings"),
    ("ai_search", "AI Search"),
    ("container_apps", "Container Apps"),
    ("cosmos_db", "Cosmos DB"),
    ("acs", "Communication Services"),
    ("key_vault", "Key Vault"),
    ("acr", "Container Registry"),
    ("foundry", "AI Foundry"),
    ("apim", "API Management"),
    ("monitor", "Azure Monitor"),
]

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
    student_id_hash: Optional[str] = Body(default=None, embed=True),
    pipeline: AllClearPipeline = Depends(get_pipeline),
) -> PipelineResult:
    """Run a signal end-to-end and return the typed PipelineResult."""
    try:
        return await pipeline.process_signal(
            text=message,
            session_id=session_id or "anonymous",
            channel=channel,
            student_id_hash=student_id_hash,
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


@router.get("/health/azure-footprint", tags=["Health"], summary="Azure footprint and rough estimate")
async def azure_footprint(settings: Settings = Depends(get_settings)) -> dict:
    """Read-only service inventory and rough monthly estimate (no billing API calls)."""
    multiplier = settings.azure_footprint_estimate_multiplier
    estimate_table = settings.azure_footprint_estimate_table
    services = []
    total = 0.0
    for key, label in AZURE_FOOTPRINT_SERVICES:
        baseline = float(estimate_table.get(key, 0.0))
        estimated = round(baseline * multiplier, 2)
        services.append(
            {
                "service_key": key,
                "service_name": label,
                "estimated_monthly_cost": estimated,
                "estimate_only": True,
            }
        )
        total += estimated

    return {
        "services": services,
        "estimate": {
            "currency": settings.azure_footprint_estimate_currency,
            "monthly_total": round(total, 2),
            "volume_multiplier": multiplier,
            "estimate_only": True,
            "disclaimer": (
                "Rough estimate from static configuration values. "
                "Not live billing data."
            ),
        },
    }


@router.get("/health/models", tags=["Health"], summary="Active model + failover chain")
async def model_status() -> dict:
    """Report the active chat model, the configured fallback chain, and the model
    that served the most recent request (018-model-agnostic-failover).

    Lets an operator (or the stage demo) see that triage keeps running on a
    fallback model if the primary is pulled or restricted.
    """
    return get_model_status()


@router.get("/demo/clearboard", tags=["Demo"], summary="Idempotent ClearBoard demo fixture")
async def demo_clearboard(
    mode: Literal["blank", "loaded"] = "loaded",
    pack: Optional[str] = None,
    settings: Settings = Depends(get_settings),
) -> dict:
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
    if pack is None:
        return DEMO_CLEARBOARD
    try:
        return clearboard_for_pack(settings, pack)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=f"Unknown scenario pack: {exc.args[0]}") from exc
    except PermissionError as exc:
        raise HTTPException(
            status_code=403, detail=f"Scenario pack is disabled by config: {exc.args[0]}"
        ) from exc


@router.get("/demo/scenario-packs", tags=["Demo"], summary="Available scenario packs")
async def demo_scenario_packs(settings: Settings = Depends(get_settings)) -> dict:
    packs = list_available_packs(settings)
    return {
        "default_pack": settings.scenario_pack_default,
        "packs": packs,
    }


@router.post(
    "/demo/scenario-packs/{pack_id}/dedup-probe",
    tags=["Demo"],
    summary="Run deterministic dedup attach probe for a scenario pack",
)
async def demo_dedup_probe(
    pack_id: str,
    pipeline: AllClearPipeline = Depends(get_pipeline),
    settings: Settings = Depends(get_settings),
) -> dict:
    try:
        first_signal, second_signal = dedup_probe_signals(settings, pack_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=f"Unknown scenario pack: {exc.args[0]}") from exc
    except PermissionError as exc:
        raise HTTPException(
            status_code=403, detail=f"Scenario pack is disabled by config: {exc.args[0]}"
        ) from exc
    first = await pipeline.process_signal(
        text=first_signal,
        session_id=f"pack-probe-{pack_id}-1",
        channel="chat",
    )
    second = await pipeline.process_signal(
        text=second_signal,
        session_id=f"pack-probe-{pack_id}-2",
        channel="chat",
    )
    return {
        "pack_id": pack_id,
        "first_outcome": first.routing.outcome.value,
        "second_outcome": second.routing.outcome.value,
        "first_incident_id": first.action.incident_id,
        "second_incident_id": second.action.incident_id,
        "attached": second.routing.outcome.value == "ATTACH_TO_INCIDENT"
        and second.action.incident_id == first.action.incident_id,
    }


@router.post("/demo/capstone/entries", tags=["Demo"], summary="Create capstone lead entry")
async def create_capstone_entry(
    payload: CapstoneLeadCreate,
    store=Depends(get_capstone_lead_store),
    settings: Settings = Depends(get_settings),
) -> dict:
    _require_capstone_demo_access(settings)
    entry = store.create(
        name=payload.name.strip(),
        agency=payload.agency.strip(),
        surge=payload.surge.strip(),
        signal_flood=payload.signal_flood.strip(),
        incident_underneath=payload.incident_underneath.strip(),
    )
    return {"entry": entry, "count": len(store.list_entries())}


@router.get("/demo/capstone/entries", tags=["Demo"], summary="List capstone lead entries")
async def list_capstone_entries(
    store=Depends(get_capstone_lead_store),
    settings: Settings = Depends(get_settings),
) -> dict:
    _require_capstone_demo_access(settings)
    entries = store.list_entries()
    return {"count": len(entries), "entries": entries}


@router.get("/demo/capstone/export", tags=["Demo"], summary="Export capstone lead entries")
async def export_capstone_entries(
    format: Literal["json", "csv"] = "json",
    store=Depends(get_capstone_lead_store),
    settings: Settings = Depends(get_settings),
) -> dict:
    _require_capstone_demo_access(settings)
    entries = store.list_entries()
    if format == "csv":
        csv_text = store.export_csv()
        return Response(
            content=csv_text,
            media_type="text/csv",
            headers={
                "Content-Disposition": "attachment; filename=all-clear-capstone-leads.csv"
            },
        )
    return {
        "count": len(entries),
        "entries": entries,
        "exported_at": "mock-mode-safe",
    }


@router.get("/demo/loadtest", tags=["Demo"], summary="Coach load-test job status")
async def demo_loadtest_status(coordinator=Depends(get_loadtest_coordinator)) -> dict:
    """Return the shared status of the coach load-test job (idle or running).

    Any browser/coach polls this to see live progress and to know whether a run
    is already in flight before starting another.
    """
    return await coordinator.status()


@router.post("/demo/loadtest", tags=["Demo"], summary="Start a coach load-test surge")
async def demo_loadtest_start(
    *,
    count: int = Body(default=40, embed=True, ge=1, le=150),
    mode: str = Body(default="varied", embed=True),
    started_by: str = Body(default="coach", embed=True),
    pack: Optional[str] = Body(default=None, embed=True),
    coordinator=Depends(get_loadtest_coordinator),
) -> dict:
    """Fire a burst of realistic signals through the live pipeline (demo surge).

    Single-flight and idempotent: if a run is already active (this browser, a
    second click, or another coach), no new run starts and the in-flight job's
    status is returned unchanged.
    """
    try:
        return await coordinator.start(
            count=count, mode=mode, started_by=started_by, pack=pack
        )
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=f"Unknown scenario pack: {exc.args[0]}") from exc
    except PermissionError as exc:
        raise HTTPException(
            status_code=403, detail=f"Scenario pack is disabled by config: {exc.args[0]}"
        ) from exc
