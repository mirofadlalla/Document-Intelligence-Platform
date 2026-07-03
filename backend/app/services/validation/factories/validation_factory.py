"""
ValidationFactory
==================
Constructs the full ordered list of validation rules.

Execution order matters:
    1. RequiredFieldsValidationRule  — gate: no point continuing if fields are absent
    2. InvoiceValidationRule         — format check
    3. VendorLookupValidationRule    — whitelist check (warning only)
    4. DiscountValidationRule        — range check
    5. TotalValidationRule           — positive-value check
    6. PriceValidationRule           — discount math & final-total comparison
    7. DeliveryValidationRule        — cross-document line item comparison
"""

from app.services.matching.cross_document_service import CrossDocumentService

from app.services.validation.rules.required_fields_rule import (
    RequiredFieldsValidationRule,
)
from app.services.validation.rules.invoice_validation import (
    InvoiceValidationRule,
)
from app.services.validation.rules.vendor_lookup_rule import (
    VendorLookupValidationRule,
)
from app.services.validation.rules.discount_validation_rule import (
    DiscountValidationRule,
)
from app.services.validation.rules.total_validation_rule import (
    TotalValidationRule,
)
from app.services.validation.rules.price_validation import (
    PriceValidationRule,
)
from app.services.validation.rules.delivery_validation import (
    DeliveryValidationRule,
)


class ValidationFactory:

    @staticmethod
    def create():

        cross_document_service = CrossDocumentService()

        return [
            RequiredFieldsValidationRule(),
            InvoiceValidationRule(),
            VendorLookupValidationRule(),
            DiscountValidationRule(),
            TotalValidationRule(),
            PriceValidationRule(),
            DeliveryValidationRule(cross_document_service),
        ]