"""
DeliveryValidationRule
=======================
Validates invoice line items against delivery line items using
CrossDocumentService.

Delegates ALL comparison logic to CrossDocumentService — no duplication.

Sets validation.line_items_match_delivery and appends mismatch errors.
"""

from app.schemas.extraction import ExtractionResult
from app.schemas.validation import ValidationResult
from app.services.matching.cross_document_service import CrossDocumentService

from .base_rule import BaseValidationRule


class DeliveryValidationRule(BaseValidationRule):

    def __init__(self, cross_document_service: CrossDocumentService) -> None:
        self._cross_document_service = cross_document_service

    def validate(
        self,
        extraction: ExtractionResult,
        validation: ValidationResult,
    ) -> None:

        # If either side has no line items, there is nothing to compare.
        if not extraction.invoice_line_items and not extraction.delivery_line_items:
            validation.line_items_match_delivery = True
            return

        result = self._cross_document_service.compare(
            invoice_items=extraction.invoice_line_items,
            delivery_items=extraction.delivery_line_items,
        )

        validation.line_items_match_delivery = result.matches

        for mismatch in result.mismatches:
            validation.warnings.append(mismatch)