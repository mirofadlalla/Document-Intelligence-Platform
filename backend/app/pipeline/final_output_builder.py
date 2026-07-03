"""
FinalOutputBuilder
==================
Fluent builder that assembles the final ProcessResponse.

Preferred usage::

    result = (
        FinalOutputBuilder()
        .metadata(source_email="sender@example.com", timestamp_processed=now)
        .extraction(extraction_result)
        .validation(validation_result)
        .workflow(workflow_action)
        .build()
    )

Output shape::

    {
        "metadata":        { "source_email": "...", "timestamp_processed": "..." },
        "extraction":      { ...ExtractionResult fields... },
        "validation":      { ...ValidationResult fields... },
        "workflow_action": "APPROVE" | "ROUTE_TO_HUMAN_REVIEW" | "REJECT"
    }

Each builder method returns `self` to enable method chaining.
`build()` validates that all required parts have been provided and
returns a fully typed `ProcessResponse` Pydantic model.
"""

from datetime import datetime, timezone

from app.schemas.api import ProcessResponse, ResponseMetadata
from app.schemas.extraction import ExtractionResult
from app.schemas.validation import ValidationResult
from app.schemas.workflow import WorkflowAction


class FinalOutputBuilder:
    """
    Fluent builder for ProcessResponse.

    Call the four setter methods in any order, then call `.build()`.
    A `ValueError` is raised if any required part is missing at build time.
    """

    def __init__(self) -> None:
        self._metadata: ResponseMetadata | None = None
        self._extraction: ExtractionResult | None = None
        self._validation: ValidationResult | None = None
        self._workflow_action: WorkflowAction | None = None

    # ------------------------------------------------------------------ #
    # Fluent setters                                                       #
    # ------------------------------------------------------------------ #

    def metadata(
        self,
        source_email: str,
        timestamp_processed: datetime | None = None,
    ) -> "FinalOutputBuilder":
        """
        Set document metadata.

        If `timestamp_processed` is omitted, the current UTC time is used.
        """
        self._metadata = ResponseMetadata(
            source_email=source_email,
            timestamp_processed=timestamp_processed or datetime.now(tz=timezone.utc),
        )
        return self

    def extraction(self, extraction_result: ExtractionResult) -> "FinalOutputBuilder":
        """Attach the extraction result."""
        self._extraction = extraction_result
        return self

    def validation(self, validation_result: ValidationResult) -> "FinalOutputBuilder":
        """Attach the validation result."""
        self._validation = validation_result
        return self

    def workflow(self, workflow_action: WorkflowAction) -> "FinalOutputBuilder":
        """Attach the workflow action."""
        self._workflow_action = workflow_action
        return self

    # ------------------------------------------------------------------ #
    # Terminal method                                                      #
    # ------------------------------------------------------------------ #

    def build(self) -> ProcessResponse:
        """
        Validates all parts are present and returns a `ProcessResponse`.

        Raises:
            ValueError: if any required part was not set.
        """
        missing = []
        if self._metadata is None:
            missing.append("metadata")
        if self._extraction is None:
            missing.append("extraction")
        if self._validation is None:
            missing.append("validation")
        if self._workflow_action is None:
            missing.append("workflow")

        if missing:
            raise ValueError(
                f"FinalOutputBuilder.build() called with missing parts: "
                f"{', '.join(missing)}"
            )

        return ProcessResponse(
            metadata=self._metadata,        # type: ignore[arg-type]
            extraction=self._extraction,    # type: ignore[arg-type]
            validation=self._validation,    # type: ignore[arg-type]
            workflow_action=self._workflow_action,  # type: ignore[arg-type]
        )
