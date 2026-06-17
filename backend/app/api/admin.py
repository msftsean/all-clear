"""Admin API endpoints for branding and ticket management.

Provides:
  GET  /api/admin/branding        – get current branding config
  PUT  /api/admin/branding        – update branding config
  GET  /api/admin/tickets         – list all tickets (with filters)
  PUT  /api/admin/tickets/{id}    – update ticket status
  DELETE /api/admin/tickets/{id}  – delete a ticket
"""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel

from app.core.dependencies import BrandingServiceDep, TicketServiceDep
from app.models.enums import Department, TicketStatus
from app.models.schemas import (
    BrandingResponse,
    BrandingUpdateRequest,
    TicketListResponse,
    TicketStatusResponse,
)

router = APIRouter(prefix="/admin", tags=["Admin"])


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
    branding_service: BrandingServiceDep,
) -> BrandingResponse:
    """Return the current institution branding configuration."""
    config = await branding_service.get_branding()
    return BrandingResponse(config=config)


@router.put("/branding", response_model=BrandingResponse, summary="Update branding config")
async def update_branding(
    request: BrandingUpdateRequest,
    branding_service: BrandingServiceDep,
) -> BrandingResponse:
    """Update the institution branding configuration (partial update — only provided fields change)."""
    config = await branding_service.update_branding(
        logo_url=request.logo_url,
        primary_color=request.primary_color,
        institution_name=request.institution_name,
        tagline=request.tagline,
    )
    return BrandingResponse(config=config)


# ---------------------------------------------------------------------------
# Ticket management
# ---------------------------------------------------------------------------

@router.get("/tickets", response_model=TicketListResponse, summary="List all tickets")
async def list_tickets(
    ticket_service: TicketServiceDep,
    ticket_status: Optional[TicketStatus] = Query(default=None, alias="status"),
    department: Optional[Department] = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    limit: Optional[int] = Query(default=None, ge=1, le=200),
) -> TicketListResponse:
    """List all tickets across all departments with optional filters."""
    # 'limit' is used by the frontend; map it to page_size when provided
    effective_page_size = limit if limit is not None else page_size
    result = await ticket_service.list_all_tickets(
        status_filter=ticket_status,
        department_filter=department,
        page=page,
        page_size=effective_page_size,
    )
    return result


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
    request: TicketUpdateRequest,
    ticket_service: TicketServiceDep,
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
    ticket_service: TicketServiceDep,
) -> dict:
    """Permanently delete a ticket."""
    success = await ticket_service.delete_ticket(ticket_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ticket {ticket_id} not found",
        )
    return {"message": f"Ticket {ticket_id} deleted successfully"}
