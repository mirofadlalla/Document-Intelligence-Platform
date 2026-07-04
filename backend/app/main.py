"""
FastAPI Application Bootstrap
==============================
Registers the application, lifespan events, and API router.

Lifespan
--------
startup  — ping MongoDB to validate connectivity (fail-fast).
shutdown — close the Motor connection pool.
"""

from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from app.core.config import settings
from app.core.logging import logger
from app.infrastructure.database import mongodb


@asynccontextmanager
async def lifespan(app: FastAPI):
    # ── startup ──────────────────────────────────────────────────────────────
    logger.info("Starting Document Intelligence Platform…")

    connected = await mongodb.ping()
    if not connected:
        logger.warning(
            "MongoDB is unreachable at startup. "
            "Persistence features will be unavailable."
        )

    yield

    # ── shutdown ─────────────────────────────────────────────────────────────
    await mongodb.close()
    logger.info("Application shut down cleanly.")


app = FastAPI(
    title="Document Intelligence Platform",
    description=(
        "Automated invoice processing pipeline: "
        "ingestion → LLM extraction → validation → workflow routing."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)


# ── Health check ─────────────────────────────────────────────────────────────

@app.get("/health", tags=["System"])
async def health() -> dict:
    """Lightweight liveness probe used by load balancers and Docker."""
    return {"status": "ok", "version": "1.0.0"}


# ── API routes (to be registered once built) ─────────────────────────────────
# from app.api.routes import processing
# app.include_router(processing.router, prefix=settings.api_prefix)


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
    )
