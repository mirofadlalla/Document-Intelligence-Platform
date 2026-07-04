from typing import Any, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from app.api.dependencies import get_repository
from app.infrastructure.database.repository import ProcessingJobRepository
from app.schemas.processing_job import ProcessingJob

router = APIRouter()

@router.get("/jobs", tags=["Jobs"])
async def list_jobs(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    workflow_action: Optional[str] = None,
    status: Optional[str] = None,
    vendor_name: Optional[str] = None,
    repository: ProcessingJobRepository = Depends(get_repository)
) -> list[ProcessingJob]:
    skip = (page - 1) * limit
    filters: dict[str, Any] = {}
    if workflow_action:
        filters["workflow_action"] = workflow_action
    if status:
        filters["status"] = status
    if vendor_name:
        filters["extraction.vendor_name"] = {"$regex": vendor_name, "$options": "i"}

    jobs = await repository.list_jobs(skip=skip, limit=limit, filters=filters)
    return jobs

@router.get("/jobs/{job_id}", tags=["Jobs"])
async def get_job(
    job_id: str,
    repository: ProcessingJobRepository = Depends(get_repository)
) -> ProcessingJob:
    job = await repository.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@router.delete("/jobs/{job_id}", tags=["Jobs"])
async def delete_job(
    job_id: str,
    repository: ProcessingJobRepository = Depends(get_repository)
) -> dict[str, str]:
    success = await repository.delete_job(job_id)
    if not success:
        raise HTTPException(status_code=404, detail="Job not found")
    return {"status": "deleted"}
