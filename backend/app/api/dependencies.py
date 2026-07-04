"""
FastAPI Dependency Injection
=============================
Provides shared dependencies for route handlers.

All pipeline components are instantiated once here and returned via
FastAPI's Depends() mechanism so every request gets the same singletons.
"""

from functools import lru_cache

from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.infrastructure.database import mongodb
from app.infrastructure.database.repository import ProcessingJobRepository
from app.infrastructure.extraction.factories.extractor_factory import ExtractorFactory
from app.pipeline.final_output_builder import FinalOutputBuilder
from app.pipeline.processing_pipeline import ProcessingPipeline
from app.services.ingestion.ingestion_service import IngestionService
from app.services.validation.services.validation_service import ValidationService
from app.services.workflow.workflow_service import WorkflowService


def get_db() -> AsyncIOMotorDatabase:
    """Return the application database handle."""
    return mongodb.get_database()


def get_repository(db: AsyncIOMotorDatabase = Depends(get_db)) -> ProcessingJobRepository:
    return ProcessingJobRepository(db)


@lru_cache(maxsize=1)
def get_ingestion_service() -> IngestionService:
    return IngestionService()


@lru_cache(maxsize=1)
def get_validation_service() -> ValidationService:
    return ValidationService()


@lru_cache(maxsize=1)
def get_workflow_service() -> WorkflowService:
    return WorkflowService()


def get_pipeline(
    repository: ProcessingJobRepository = Depends(get_repository),
) -> ProcessingPipeline:
    return ProcessingPipeline(
        ingestion_service=get_ingestion_service(),
        extractor=ExtractorFactory.create(),
        validation_service=get_validation_service(),
        workflow_service=get_workflow_service(),
        output_builder=FinalOutputBuilder(),
        repository=repository,
    )
