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

            validation.errors.append(
                "Invoice number is missing."
            )

            return

        if not re.match(
            self.INVOICE_REGEX,
            extraction.invoice_number,
        ):

            validation.errors.append(
                "Invalid invoice number format."
            )

# InvoiceValidationRule
# مسئولة عن
# Regex
# Invoice Number
# Format
# Missing fields
