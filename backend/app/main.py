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
from fastapi.middleware.cors import CORSMiddleware

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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── API routes ───────────────────────────────────────────────────────────────
from app.api.routes import router as api_router
app.include_router(api_router, prefix="/api/v1")

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
    )
