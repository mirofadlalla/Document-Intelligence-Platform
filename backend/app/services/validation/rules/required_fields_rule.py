"""
RequiredFieldsValidationRule
=============================
Validates that all mandatory fields are present in the extraction result.

Required fields:
    - vendor_name
    - invoice_number
    - raw_total

Sets validation.required_fields_valid = True only when ALL fields are present.
"""

from app.schemas.extraction import ExtractionResult
from app.schemas.validation import ValidationResult

from .base_rule import BaseValidationRule


class RequiredFieldsValidationRule(BaseValidationRule):

    REQUIRED_FIELDS: list[tuple[str, str]] = [
        ("vendor_name",    "Vendor name is missing."),
        ("invoice_number", "Invoice number is missing."),
        ("raw_total",      "Raw total is missing."),
    ]

    def validate(
        self,
        extraction: ExtractionResult,
        validation: ValidationResult,
    ) -> None:

        all_present = True

        for field_name, error_message in self.REQUIRED_FIELDS:
            value = getattr(extraction, field_name, None)
            if value is None:
                validation.errors.append(error_message)
                all_present = False

        validation.required_fields_valid = all_present
