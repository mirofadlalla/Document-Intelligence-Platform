"""
InvoiceValidationRule
======================
Validates invoice number format via regex.

Expected format: INV-<4-digit year>-<digits>
Example: INV-2026-00125

Sets validation.invoice_number_valid = True on success.
"""

import re

from app.schemas.extraction import ExtractionResult
from app.schemas.validation import ValidationResult

from .base_rule import BaseValidationRule


class InvoiceValidationRule(BaseValidationRule):

    INVOICE_REGEX = r"^INV-\d{4}-\d+$"

    def validate(
        self,
        extraction: ExtractionResult,
        validation: ValidationResult,
    ) -> None:

        if extraction.invoice_number is None:
            # RequiredFieldsValidationRule already reported this as an error.
            validation.invoice_number_valid = False
            return

        if re.match(self.INVOICE_REGEX, extraction.invoice_number):
            validation.invoice_number_valid = True
        else:
            validation.invoice_number_valid = False
            validation.errors.append(
                f"Invalid invoice number format: '{extraction.invoice_number}'. "
                "Expected format: INV-YYYY-NNNNN (e.g. INV-2026-00125)."
            )


# InvoiceValidationRule
# مسئولة عن
# Regex
# Invoice Number
# Format
# Missing fields
