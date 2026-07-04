"""
ProcessingPipeline
==================
Single entry point for the entire document processing business flow.

This class contains NO business logic.
It only orchestrates existing components in a fixed, deterministic order.

Flow
----
Incoming Email + File Paths
        ↓
IngestionService       — parse attachments → list[Attachment]
        ↓
BaseExtractor          — LLM extraction   → ExtractionResult
        ↓
ValidationService      — run all rules    → ValidationResult
        ↓
WorkflowService        — decide action    → WorkflowResult
        ↓
FinalOutputBuilder     — assemble output  → ProcessResponse
        ↓
ProcessingJobRepository — persist job     → job_id stored
        ↓
ProcessResponse        — returned to caller

All components are injected via the constructor (DI).
The pipeline itself is stateless after __init__.
"""

from app.core.logging import logger
from app.infrastructure.database.repository import ProcessingJobRepository
from app.infrastructure.extraction.strategies.base_extractor import BaseExtractor
from app.pipeline.final_output_builder import FinalOutputBuilder
from app.schemas.api import ProcessRequest, ProcessResponse
from app.schemas.processing_job import ProcessingJob, ProcessingStatus
from app.schemas.api import ResponseMetadata
from app.services.ingestion.ingestion_service import IngestionService
from app.services.validation.services.validation_service import ValidationService
from app.services.workflow.workflow_service import WorkflowService

from datetime import datetime, timezone


class ProcessingPipeline:
    """
    Orchestrates the full deterministic document processing flow.

    Parameters
    ----------
    ingestion_service:
        Parses raw file paths into structured Attachment objects.
    extractor:
        LLM strategy that extracts structured business data from email + attachments.
    validation_service:
        Runs all deterministic validation rules against the extraction result.
    workflow_service:
        Decides the routing action based solely on the validation result.
    output_builder:
        Fluent builder that assembles the final ProcessResponse.
    repository:
        Persists the ProcessingJob record throughout the pipeline.
    """

    def __init__(
        self,
        ingestion_service: IngestionService,
        extractor: BaseExtractor,
        validation_service: ValidationService,
        workflow_service: WorkflowService,
        output_builder: FinalOutputBuilder,
        repository: ProcessingJobRepository,
    ) -> None:
        self._ingestion = ingestion_service
        self._extractor = extractor
        self._validation = validation_service
        self._workflow = workflow_service
        self._output_builder = output_builder
        self._repository = repository

    async def process(
        self,
        request: ProcessRequest,
        file_paths: list[str],
        source_email: str,
    ) -> ProcessResponse:
        """
        Execute the full pipeline for one incoming email.

        Parameters
        ----------
        request:
            Email subject + body from the API layer.
        file_paths:
            Absolute paths to uploaded attachment files.
        source_email:
            Sender address — stored in job metadata.

        Returns
        -------
        ProcessResponse
            Fully assembled output including extraction, validation, and
            routing decision.

        Raises
        ------
        Exception
            Any unhandled error is logged, the job status is set to FAILED,
            and the exception is re-raised so the API layer can return a 500.
        """
        now = datetime.now(tz=timezone.utc)

        # ------------------------------------------------------------------ #
        # Initialise job record                                               #
        # ------------------------------------------------------------------ #
        job = ProcessingJob(
            status=ProcessingStatus.RECEIVED,
            metadata=ResponseMetadata(
                source_email=source_email,
                timestamp_processed=now,
            ),
        )
        job_id = await self._repository.save(job)
        logger.info("Pipeline started: job_id=%s", job_id)

        try:
            # -------------------------------------------------------------- #
            # Step 1 — Attachment parsing                                      #
            # -------------------------------------------------------------- #
            await self._repository.update_status(job_id, ProcessingStatus.PARSING)
            logger.info("[%s] Parsing %d attachment(s).", job_id, len(file_paths))

            attachments = self._ingestion.parse_documents(file_paths)

            # -------------------------------------------------------------- #
            # Step 2 — LLM extraction                                          #
            # -------------------------------------------------------------- #
            await self._repository.update_status(job_id, ProcessingStatus.EXTRACTING)
            logger.info("[%s] Running LLM extraction.", job_id)

            extraction = await self._extractor.extract(
                subject=request.subject,
                body=request.body,
                attachments=attachments,
            )

            # -------------------------------------------------------------- #
            # Step 3 — Validation                                              #
            # -------------------------------------------------------------- #
            await self._repository.update_status(job_id, ProcessingStatus.VALIDATING)
            logger.info("[%s] Running validation.", job_id)

            validation = self._validation.validate(extraction)

            # -------------------------------------------------------------- #
            # Step 4 — Workflow decision                                       #
            # -------------------------------------------------------------- #
            workflow_result = self._workflow.decide(validation)
            logger.info(
                "[%s] Workflow decision: %s", job_id, workflow_result.action.value
            )

            # -------------------------------------------------------------- #
            # Step 5 — Assemble final response                                 #
            # -------------------------------------------------------------- #
            response = (
                FinalOutputBuilder()
                .metadata(
                    source_email=source_email,
                    timestamp_processed=now,
                )
                .extraction(extraction)
                .validation(validation)
                .workflow(workflow_result.action)
                .build()
            )

            # -------------------------------------------------------------- #
            # Step 6 — Persist completed job                                   #
            # -------------------------------------------------------------- #
            await self._repository.update_status(
                job_id,
                ProcessingStatus.COMPLETED,
                extra_fields={
                    "attachments": [a.model_dump(mode="json") for a in attachments],
                    "extraction": extraction.model_dump(mode="json"),
                    "validation": validation.model_dump(mode="json"),
                    "workflow_action": workflow_result.action.value,
                },
            )
            logger.info("[%s] Pipeline completed successfully.", job_id)

            return response

        except Exception as exc:
            logger.error("[%s] Pipeline failed: %s", job_id, exc, exc_info=True)
            await self._repository.update_status(
                job_id,
                ProcessingStatus.FAILED,
                extra_fields={"error_message": str(exc)},
            )
            raise
