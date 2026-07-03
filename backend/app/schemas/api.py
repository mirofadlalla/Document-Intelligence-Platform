from datetime import datetime

from pydantic import BaseModel

from app.schemas.extraction import ExtractionResult
from app.schemas.validation import ValidationResult
from app.schemas.workflow import WorkflowAction


class ProcessRequest(BaseModel):

    subject: str

    body: str


class ResponseMetadata(BaseModel):
    """Metadata attached to every processed document response."""

    source_email: str

    timestamp_processed: datetime


class ProcessResponse(BaseModel):
    """
    Final output shape:

    {
        "metadata":        { "source_email": "...", "timestamp_processed": "..." },
        "extraction":      { ... ExtractionResult fields ... },
        "validation":      { ... ValidationResult fields ... },
        "workflow_action": "APPROVE" | "ROUTE_TO_HUMAN_REVIEW" | "REJECT"
    }
    """

    metadata: ResponseMetadata

    extraction: ExtractionResult

    validation: ValidationResult

    workflow_action: WorkflowAction