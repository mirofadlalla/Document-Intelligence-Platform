from typing import Any
from fastapi import APIRouter, Depends
from app.api.dependencies import get_repository
from app.infrastructure.database.repository import ProcessingJobRepository

router = APIRouter()

@router.get("/statistics", tags=["Statistics"])
async def get_statistics(
    repository: ProcessingJobRepository = Depends(get_repository)
) -> dict[str, Any]:
    stats = await repository.get_statistics()
    return stats
