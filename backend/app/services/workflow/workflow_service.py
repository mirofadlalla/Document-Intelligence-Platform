"""
WorkflowService
================
Decides the workflow action based solely on the ValidationResult.

This service has zero knowledge of:
    - email structure
    - LLM providers
    - extraction schema
    - OCR / document parsing

Data flow:
    ExtractionResult
        ↓
    ValidationService   ← converts business signals to warnings
        ↓
    ValidationResult
        ↓
    WorkflowService     ← inspects only errors & warnings
        ↓
    WorkflowResult

Decision priority (first matching rule wins):
    1. REJECT              — validation.errors is non-empty
    2. ROUTE_TO_HUMAN_REVIEW — validation.warnings is non-empty
    3. APPROVE             — everything is clean
"""

from app.schemas.validation import ValidationResult
from app.schemas.workflow import WorkflowAction, WorkflowResult


class WorkflowService:
    """
    Usage::

        service = WorkflowService()
        result = service.decide(validation)
        # result.action -> WorkflowAction
        # result.reason -> str
    """

    def decide(self, validation: ValidationResult) -> WorkflowResult:

        # ------------------------------------------------------------------ #
        # 1. REJECT — any hard error exists                                   #
        #    Examples: missing required fields, invalid invoice format,       #
        #    negative totals, discount > 100, price calculation mismatch.     #
        # ------------------------------------------------------------------ #
        if validation.errors:
            return WorkflowResult(
                action=WorkflowAction.REJECT,
                reason=(
                    f"Document rejected due to {len(validation.errors)} "
                    f"validation error(s): "
                    + "; ".join(validation.errors)
                ),
            )

        # ------------------------------------------------------------------ #
        # 2. ROUTE_TO_HUMAN_REVIEW — any warning exists                      #
        #    Examples: unknown vendor, line-item mismatch, urgent flag,       #
        #    manual routing instruction.                                      #
        # ------------------------------------------------------------------ #
        if validation.warnings:
            return WorkflowResult(
                action=WorkflowAction.REVIEW,
                reason=(
                    f"Document routed for human review due to "
                    f"{len(validation.warnings)} warning(s): "
                    + "; ".join(validation.warnings)
                ),
            )

        # ------------------------------------------------------------------ #
        # 3. APPROVE — no errors, no warnings                                #
        # ------------------------------------------------------------------ #
        return WorkflowResult(
            action=WorkflowAction.APPROVE,
            reason="All validation checks passed. Document approved.",
        )
