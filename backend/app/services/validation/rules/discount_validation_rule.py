"""
DiscountValidationRule
========================
Validates that the applied discount percentage is within the legal range.

Valid range: 0 <= discount <= 100

Negative discounts or discounts above 100 are hard errors that trigger REJECT.
"""

from app.schemas.extraction import ExtractionResult
from app.schemas.validation import ValidationResult

from .base_rule import BaseValidationRule


class DiscountValidationRule(BaseValidationRule):

    MIN_DISCOUNT: float = 0.0
    MAX_DISCOUNT: float = 100.0

    def validate(
        self,
        extraction: ExtractionResult,
        validation: ValidationResult,
    ) -> None:

        discount = extraction.applied_discount_percentage

        # Discount is optional — no value means no discount applied.
        if discount is None:
            return

        if discount < self.MIN_DISCOUNT:
            validation.errors.append(
                f"Invalid discount: {discount}% is negative. "
                "Discount must be >= 0."
            )
        elif discount > self.MAX_DISCOUNT:
            validation.errors.append(
                f"Invalid discount: {discount}% exceeds 100%. "
                "Discount must be <= 100."
            )
