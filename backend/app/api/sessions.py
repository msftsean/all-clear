"""Fail-closed conversation history endpoints.

History retrieval needs a server-verified principal-to-session ownership
contract. The current API has no such contract, so these routes intentionally
remain unavailable rather than trusting caller-supplied session IDs or hashes.
"""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, HTTPException, status

router = APIRouter(prefix="/sessions", tags=["Sessions"])

_HISTORY_UNAVAILABLE = (
    "Conversation history is unavailable until authenticated ownership is configured."
)


@router.get(
    "/{session_id}",
    summary="Get a single session with full conversation history",
)
async def get_session(session_id: UUID) -> None:
    """Reject access until a trusted owner can be established server-side."""
    raise HTTPException(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        detail=_HISTORY_UNAVAILABLE,
    )


@router.get(
    "",
    summary="List sessions for an authenticated owner",
    description=(
        "Unavailable until the backend can derive session ownership from a "
        "verified server-side identity. Caller-supplied hashes are not authorization."
    ),
)
async def list_sessions() -> None:
    """Reject history listing until authenticated ownership is available."""
    raise HTTPException(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        detail=_HISTORY_UNAVAILABLE,
    )
