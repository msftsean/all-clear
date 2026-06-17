"""
Session history API endpoints (019-conversation-persistence).

Provides read-only access to persisted conversation sessions:
  GET /api/sessions/{session_id}    – retrieve a single session with full history
  GET /api/sessions                 – list sessions for a student (by student_id_hash)

Constitution Art. III: student_id_hash is the only student identifier accepted
or returned; raw student IDs are never logged or stored here.
"""

from __future__ import annotations

from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.core.dependencies import get_session_store
from app.models.schemas import Session
from app.services.interfaces import SessionStoreInterface

router = APIRouter(prefix="/sessions", tags=["Sessions"])


@router.get(
    "/{session_id}",
    response_model=Session,
    summary="Get a single session with full conversation history",
)
async def get_session(
    session_id: UUID,
    store: SessionStoreInterface = Depends(get_session_store),
) -> Session:
    """Return the full session record including all conversation turns."""
    session = await store.get_session(session_id)
    if session is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session {session_id} not found.",
        )
    return session


@router.get(
    "",
    response_model=list[Session],
    summary="List sessions for a student",
    description=(
        "Returns sessions for the given student_id_hash, newest first. "
        "student_id_hash must be a 64-character hex SHA-256 of the anonymous "
        "browser identity token."
    ),
)
async def list_sessions(
    student_id_hash: str = Query(
        ...,
        min_length=64,
        max_length=64,
        description="SHA-256 hex of anonymous student identity token",
    ),
    limit: int = Query(default=20, ge=1, le=100),
    store: SessionStoreInterface = Depends(get_session_store),
) -> list[Session]:
    """Return up to ``limit`` sessions for the given student, newest first."""
    return await store.get_sessions_by_student(student_id_hash, limit=limit)
