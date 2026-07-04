"""
RequiredFieldsValidationRule
=============================
Validates that all mandatory fields are present in the extraction result.

Required fields:
    - vendor_name
    - invoice_number
    - subtotal OR raw_total (backward compatibility)

Sets validation.required_fields_valid = True only when ALL fields are present.
"""

from app.schemas.extraction import ExtractionResult
from app.schemas.validation import ValidationResult

from .base_rule import BaseValidationRule


class RequiredFieldsValidationRule(BaseValidationRule):

    REQUIRED_FIELDS: list[tuple[str, str]] = [
        ("vendor_name", "Vendor name is missing."),
        ("invoice_number", "Invoice number is missing."),
    ]

    def validate(
        self,
        extraction: ExtractionResult,
        validation: ValidationResult,
    ) -> None:

        all_present = True

        # Validate standard required fields
        for field_name, error_message in self.REQUIRED_FIELDS:
            value = getattr(extraction, field_name, None)

            if value is None:
                validation.errors.append(error_message)
                all_present = False

        # Validate subtotal with backward compatibility.
        # Accept either:
        # - subtotal (new schema)
        # - raw_total (legacy schema)
        if extraction.subtotal is None and extraction.raw_total is None:
            validation.errors.append(
                "Invoice subtotal is missing."
            )
            all_present = False

        validation.required_fields_valid = all_present