"""Call-scoped phone transcript SSE support; public access currently fails closed."""

import asyncio
import json
import logging

from fastapi import APIRouter, HTTPException, Request, status
from fastapi.responses import StreamingResponse

from app.services.transcript_bus import transcript_bus

logger = logging.getLogger(__name__)

router = APIRouter()


async def _event_generator(request: Request, call_id: str):
    """Yield redacted events for one server-authorized call until disconnect."""
    async with transcript_bus.subscribe(call_id=call_id) as queue:
        while True:
            if await request.is_disconnected():
                break
            try:
                event = await asyncio.wait_for(queue.get(), timeout=15.0)
                yield f"data: {json.dumps(event)}\n\n"
            except asyncio.TimeoutError:
                # Send keepalive comment to prevent proxy/browser timeout
                yield ": keepalive\n\n"


@router.get("/transcripts/stream")
async def stream_transcripts() -> StreamingResponse:
    """Fail closed until the request can be bound to an authorized phone call."""
    raise HTTPException(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        detail=(
            "Phone transcripts are unavailable until authenticated call ownership "
            "is configured."
        ),
    )
