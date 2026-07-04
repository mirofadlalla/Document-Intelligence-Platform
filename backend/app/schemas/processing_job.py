"""
ProcessingJob
=============
Persistent record that tracks the full lifecycle of one email processing request.

ProcessingStatus
----------------
Tracks which pipeline stage the job is currently in.
Used by the repository layer — never exposed as business logic.
"""

from datetime import datetime, timezone
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field

from app.schemas.api import ResponseMetadata
from app.schemas.attachment import Attachment
from app.schemas.extraction import ExtractionResult
from app.schemas.validation import ValidationResult
from app.schemas.workflow import WorkflowAction


class ProcessingStatus(str, Enum):
    RECEIVED = "RECEIVED"
    PARSING = "PARSING"
    EXTRACTING = "EXTRACTING"
    VALIDATING = "VALIDATING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class ProcessingJob(BaseModel):
    """
    Full snapshot of a single document processing run.

    Fields
    ------
    job_id:
        Unique identifier assigned at creation (MongoDB ObjectId as string).
    status:
        Current lifecycle stage.
    metadata:
        Source email address and timestamp.
    attachments:
        Parsed document records produced by IngestionService.
    extraction:
        LLM extraction result (None until extraction completes).
    validation:
        Validation result (None until validation completes).
    workflow_action:
        Final routing decision (None until workflow is decided).
    error_message:
        Populated only when status == FAILED.
    created_at / updated_at:
        UTC timestamps managed by the repository layer.
    """

    job_id: Optional[str] = None

    status: ProcessingStatus = ProcessingStatus.RECEIVED

    metadata: ResponseMetadata

    attachments: list[Attachment] = Field(default_factory=list)

    extraction: Optional[ExtractionResult] = None

    validation: Optional[ValidationResult] = None

    workflow_action: Optional[WorkflowAction] = None

    error_message: Optional[str] = None

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(tz=timezone.utc)
    )

    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(tz=timezone.utc)
    )