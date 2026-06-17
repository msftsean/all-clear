"""Admin API endpoints for branding and ticket management.

Provides:
  GET  /api/admin/branding        – get current branding config
  PUT  /api/admin/branding        – update branding config
  GET  /api/admin/tickets         – list all tickets (with filters)
  PUT  /api/admin/tickets/{id}    – update ticket status
  DELETE /api/admin/tickets/{id}  – delete a ticket
"""

from typing import Annotated, Optional

from fastapi import APIRouter, Body, Depends, HTTPException, Query, status
from pydantic import BaseModel

from app.core.dependencies import get_branding_service, get_ticket_service
from app.models.enums import Department, TicketStatus
from app.models.schemas import (
    BrandingResponse,
    BrandingUpdateRequest,
    TicketListResponse,
    TicketStatusResponse,
)
from app.services.interfaces import BrandingServiceInterface, TicketServiceInterface

router = APIRouter(prefix="/admin", tags=["Admin"])


def _branding_service_dep() -> BrandingServiceInterface:
    """FastAPI-safe dependency for branding service (no exposed query params)."""
    return get_branding_service()


def _ticket_service_dep() -> TicketServiceInterface:
    """FastAPI-safe dependency for ticket service (no exposed query params)."""
    return get_ticket_service()


BrandingDep = Annotated[BrandingServiceInterface, Depends(_branding_service_dep)]
TicketDep = Annotated[TicketServiceInterface, Depends(_ticket_service_dep)]


class TicketUpdateRequest(BaseModel):
    """Request body for updating a ticket (matches frontend TicketUpdateRequest)."""
    status: TicketStatus
    assigned_to: Optional[str] = None
    resolution_summary: Optional[str] = None


# ---------------------------------------------------------------------------
# Branding
# ---------------------------------------------------------------------------

@router.get("/branding", response_model=BrandingResponse, summary="Get branding config")
async def get_branding(
    branding_service: BrandingDep,
) -> BrandingResponse:
    """Return the current institution branding configuration."""
    config = await branding_service.get_branding()
    return BrandingResponse(config=config)


@router.put("/branding", response_model=BrandingResponse, summary="Update branding config")
async def update_branding(
    branding_service: BrandingDep,
    update: BrandingUpdateRequest = Body(...),
) -> BrandingResponse:
    """Update the institution branding configuration (partial update — only provided fields change)."""
    config = await branding_service.update_branding(
        logo_url=update.logo_url,
        primary_color=update.primary_color,
        institution_name=update.institution_name,
        tagline=update.tagline,
    )
    return BrandingResponse(config=config)


# ---------------------------------------------------------------------------
# Ticket management
# ---------------------------------------------------------------------------

@router.get("/tickets", response_model=TicketListResponse, summary="List all tickets")
async def list_tickets(
    ticket_service: TicketDep,
    ticket_status: Optional[TicketStatus] = Query(default=None, alias="status"),
    department: Optional[Department] = Query(default=None),
    limit: int = Query(default=50, ge=1, le=200),
) -> TicketListResponse:
    """List all tickets across all departments with optional filters."""
    tickets = await ticket_service.list_all_tickets(
        status_filter=ticket_status,
        department_filter=department,
        limit=limit,
    )
    return TicketListResponse(tickets=tickets, total=len(tickets))


@router.patch(
    "/tickets/{ticket_id}",
    response_model=TicketStatusResponse,
    summary="Update ticket status",
)
@router.put(
    "/tickets/{ticket_id}",
    response_model=TicketStatusResponse,
    summary="Update ticket status (PUT alias)",
)
async def update_ticket(
    ticket_id: str,
    ticket_service: TicketDep,
    request: TicketUpdateRequest = Body(...),
) -> TicketStatusResponse:
    """Update the status (and optionally assigned_to / resolution) of a ticket."""
    result = await ticket_service.update_ticket_status(
        ticket_id=ticket_id,
        new_status=request.status,
        assigned_to=request.assigned_to,
        resolution_summary=request.resolution_summary,
    )
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ticket {ticket_id} not found",
        )
    return result


@router.delete(
    "/tickets/{ticket_id}",
    summary="Delete a ticket",
)
async def delete_ticket(
    ticket_id: str,
    ticket_service: TicketDep,
) -> dict:
    """Permanently delete a ticket."""
    success = await ticket_service.delete_ticket(ticket_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ticket {ticket_id} not found",
        )
    return {"message": f"Ticket {ticket_id} deleted successfully"}
