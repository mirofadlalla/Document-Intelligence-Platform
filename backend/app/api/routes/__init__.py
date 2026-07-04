from fastapi import APIRouter
from app.api.routes import health, jobs, processing, statistics

router = APIRouter()

router.include_router(health.router)
router.include_router(jobs.router)
router.include_router(processing.router)
router.include_router(statistics.router)
