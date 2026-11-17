"""Room Surge API (024-room-surge).

Audience members report from their phones (`POST /report`); the room display
polls the tally (`GET /state`); the presenter opens, closes and resets the room
(`POST /control`, coach key required).

Every audience Signal goes through the unchanged AllClearPipeline on channel
``report``. This module adds admission (open/closed, per-device rate limit) and
a tally; it never classifies, routes, or touches dedup/severity/escalation.
The card id is tallied only and never reaches the pipeline.
"""

from __future__ import annotations

import hmac
import logging
import time
from typing import Literal, Optional

from fastapi import APIRouter, Depends, Header, HTTPException, status
from pydantic import BaseModel, Field

from app.agents.pipeline import AllClearPipeline
from app.api.routes import _is_content_safety_block
from app.core.config import Settings, get_settings
from app.core.dependencies import get_pipeline, get_surge_room
from app.services.surge_room import SurgeRoom, normalize_card

logger = logging.getLogger(__name__)

router = APIRouter()

BLOCKED_MESSAGE = (
    "Blocked by the safety filter, so nothing was created. That's the guardrail working."
)
ROOM_RESET_NOTICE = (
    "The room was reset while it was processing, so this response is not included "
    "in the current room tally."
)


class SurgeReportIn(BaseModel):
    message: str = Field(..., min_length=1, max_length=500)
    device_id: str = Field(..., pattern=r"^[A-Za-z0-9-]{8,64}$")
    card: Optional[str] = Field(default=None, max_length=8)


class SurgeControlIn(BaseModel):
    action: Literal["open", "close", "reset"]


def _require_coach(settings: Settings, key: Optional[str]) -> None:
    expected = settings.surge_coach_key
    if not expected:
        if settings.use_mock_services:
            return  # offline rehearsal: no key needed
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Surge control is disabled: SURGE_COACH_KEY is not set.",
        )
    if not key or not hmac.compare_digest(key.encode(), expected.encode()):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid surge key.")


@router.get("/state", summary="Room surge tally (counts and tiles; never raw text)")
async def surge_state(room: SurgeRoom = Depends(get_surge_room)) -> dict:
    return room.snapshot()


@router.post("/control", summary="Open, close or reset the room surge (coach key)")
async def surge_control(
    payload: SurgeControlIn,
    x_surge_key: Optional[str] = Header(default=None),
    room: SurgeRoom = Depends(get_surge_room),
    settings: Settings = Depends(get_settings),
) -> dict:
    _require_coach(settings, x_surge_key)
    if payload.action == "open":
        room.open()
    elif payload.action == "close":
        room.close()
    else:
        room.reset()
    return room.snapshot()


@router.post("/report", summary="Submit an audience report during the room surge")
async def surge_report(
    payload: SurgeReportIn,
    room: SurgeRoom = Depends(get_surge_room),
    pipeline: AllClearPipeline = Depends(get_pipeline),
) -> dict:
    if not room.is_open:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="The room surge isn't open right now. Watch the screen for the go signal.",
        )
    if not room.admit(payload.device_id):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="That's a lot of reports from one phone. Give it a minute.",
        )

    card = normalize_card(payload.card)
    generation = room.generation
    started = time.perf_counter()
    try:
        result = await pipeline.process_signal(
            text=payload.message,
            session_id=f"surge-{payload.device_id}",
            channel="report",
        )
    except Exception as exc:  # noqa: BLE001 - translate safety blocks; count others
        if _is_content_safety_block(exc):
            room_counted = room.record_blocked(card, generation=generation)
            message = BLOCKED_MESSAGE
            if not room_counted:
                message = f"{message} {ROOM_RESET_NOTICE}"
            print(
                f"surge_report_phases outcome=blocked "
                f"total_ms={(time.perf_counter() - started) * 1000:.1f}",
                flush=True,
            )
            return {
                "accepted": False,
                "outcome": "blocked",
                "message": message,
                "room_counted": room_counted,
            }
        room.record_failed(generation=generation)
        logger.exception("surge report failed")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="All Clear is busy. Try again in a few seconds.",
        ) from exc

    summary = room.record_result(card, result, generation=generation)
    print(
        f"surge_report_phases outcome={result.routing.outcome.value} "
        f"category={result.classification.intent_category.value} "
        f"total_ms={(time.perf_counter() - started) * 1000:.1f}",
        flush=True,
    )
    message = result.action.user_message
    if not summary["room_counted"]:
        message = f"{message} {ROOM_RESET_NOTICE}"
    return {
        "accepted": True,
        **summary,
        "severity": result.action.severity.value,
        "message": message,
    }
