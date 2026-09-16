"""Shared fail-closed auth dependencies for sensitive demo/operator routes."""

from __future__ import annotations

import hmac
from typing import Annotated

from fastapi import Depends, Header, HTTPException, status

from app.core.config import Settings, get_settings


def _constant_time_match(actual: str | None, expected: str) -> bool:
    return bool(actual) and hmac.compare_digest(actual, expected)


def verify_admin(
    x_admin_token: Annotated[str | None, Header(alias="X-Admin-Token")] = None,
    settings: Settings = Depends(get_settings),
) -> None:
    """Require the configured admin shared secret.

    The dependency intentionally fails closed when ``ADMIN_API_TOKEN`` is unset.
    That keeps public Codespaces/mock deployments from exposing admin, transcript,
    capstone export, or coach load-test surfaces by accident.
    """
    if not settings.admin_api_token:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Admin API token is not configured.",
        )
    if not _constant_time_match(x_admin_token, settings.admin_api_token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid admin token.",
        )


def verify_phone_webhook(
    x_webhook_token: Annotated[str | None, Header(alias="X-Webhook-Token")] = None,
    settings: Settings = Depends(get_settings),
) -> None:
    """Require a shared Event Grid/ACS webhook token outside mock mode.

    Mock mode remains offline-testable. Live mode refuses to process incoming or
    callback webhooks unless ``PHONE_WEBHOOK_SECRET`` is set and presented.
    """
    if settings.use_mock_services:
        return
    if not settings.phone_webhook_secret:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Phone webhook secret is not configured.",
        )
    if not _constant_time_match(x_webhook_token, settings.phone_webhook_secret):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid phone webhook token.",
        )
