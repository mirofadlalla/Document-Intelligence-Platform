"""
VendorLookupValidationRule
===========================
Validates the vendor name against a deterministic whitelist.

Unknown vendors produce a WARNING, not an error, so the document
is routed for human review rather than hard-rejected.

Sets validation.vendor_exists = True when the vendor is on the whitelist.
"""

from app.schemas.extraction import ExtractionResult
from app.schemas.validation import ValidationResult

from .base_rule import BaseValidationRule


APPROVED_VENDORS: frozenset[str] = frozenset(
    {
        "ABC TECHNOLOGIES LTD.",
        "XYZ INDUSTRIES",
        "Global Supplies Ltd.",
    }
)


class VendorLookupValidationRule(BaseValidationRule):

    def validate(
        self,
        extraction: ExtractionResult,
        validation: ValidationResult,
    ) -> None:

        if extraction.vendor_name is None:
            # RequiredFieldsValidationRule already added an error for this.
            # Do not duplicate; mark as not found.
            validation.vendor_exists = False
            return

        if extraction.vendor_name in APPROVED_VENDORS:
            validation.vendor_exists = True
        else:
            validation.vendor_exists = False
            validation.warnings.append(
                f"Vendor '{extraction.vendor_name}' is not in the approved vendor list."
            )
