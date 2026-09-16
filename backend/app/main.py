"""
FastAPI application entry point for All Clear.
"""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import router
from app.api.admin import router as admin_router
from app.api.media_ws import router as media_ws_router
from app.api.phone import router as phone_router
from app.api.realtime import router as realtime_router
from app.api.sessions import router as sessions_router
from app.api.transcripts import router as transcripts_router
from app.core.config import get_settings


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan handler for startup/shutdown."""
    # Startup
    settings = get_settings()
    print(f"Starting {settings.app_name} v{settings.app_version}")
    print(f"Environment: {settings.environment}")
    print(f"Mock mode: {settings.use_mock_services}")

    missing = settings.missing_live_settings()
    if missing:
        bar = "=" * 72
        print(bar)

    blockers = settings.live_mode_blockers()
    if blockers:
        joined = "; ".join(blockers)
        raise RuntimeError(f"Live mode blocked: {joined}")
        print("WARNING: LIVE mode (MOCK_MODE=false) but required Azure settings are missing:")
        for name in missing:
            print(f"  - {name}")
        print("The app will fail when it first calls these services (DB / search / LLM).")
        print("Fix: set them in backend/.env, or set MOCK_MODE=true to run fully offline.")
        print(bar)

    yield

    # Shutdown
    print("Shutting down...")


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    settings = get_settings()

    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="""
        All Clear incident-triage API.

        A three-stage pipeline processes inbound signals: QueryAgent classifies,
        RouterExecutor deterministically deduplicates and maps severity/SLA, and
        ActionAgent opens or attaches incidents through bounded tools.

        Mock mode is the workshop default and requires no Azure credentials.
        Live Azure integrations are optional and must be configured explicitly.
        """,
        openapi_url=f"{settings.api_prefix}/openapi.json",
        docs_url=f"{settings.api_prefix}/docs",
        redoc_url=f"{settings.api_prefix}/redoc",
        lifespan=lifespan,
    )

    origins = list(settings.allowed_origins)
    import os

    codespace_name = os.getenv("CODESPACE_NAME")
    if codespace_name:
        origins.extend(
            [
                f"https://{codespace_name}-5173.app.github.dev",
                f"https://{codespace_name}-3000.app.github.dev",
            ]
        )
    origins = sorted(set(origins))

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include API routes
    app.include_router(router, prefix=settings.api_prefix)
    app.include_router(admin_router, prefix=settings.api_prefix, tags=["Admin"])
    app.include_router(realtime_router, prefix=f"{settings.api_prefix}/realtime", tags=["Voice Realtime"])
    app.include_router(phone_router, prefix=f"{settings.api_prefix}/phone", tags=["Phone Call Automation"])
    app.include_router(transcripts_router, prefix=f"{settings.api_prefix}/phone", tags=["Phone Transcripts"])
    app.include_router(media_ws_router, prefix="/ws", tags=["Media WebSocket"])
    app.include_router(sessions_router, prefix=settings.api_prefix)

    return app


# Create the application instance
app = create_app()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
