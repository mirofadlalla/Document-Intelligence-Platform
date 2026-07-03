"""
TotalValidationRule
====================
Validates that financial totals are positive non-zero values.

Checks:
    - raw_total > 0
    - invoice_final_total > 0  (only when present)

Zero or negative totals are hard errors that trigger REJECT.
"""

from app.schemas.extraction import ExtractionResult
from app.schemas.validation import ValidationResult

from .base_rule import BaseValidationRule


class TotalValidationRule(BaseValidationRule):

    def validate(
        self,
        extraction: ExtractionResult,
        validation: ValidationResult,
    ) -> None:

        if extraction.raw_total is not None:
            if extraction.raw_total <= 0:
                validation.errors.append(
                    f"Invalid raw_total: {extraction.raw_total}. "
                    "Total must be a positive non-zero value."
                )

        if extraction.invoice_final_total is not None:
            if extraction.invoice_final_total <= 0:
                validation.errors.append(
                    f"Invalid invoice_final_total: {extraction.invoice_final_total}. "
                    "Total must be a positive non-zero value."
                )
