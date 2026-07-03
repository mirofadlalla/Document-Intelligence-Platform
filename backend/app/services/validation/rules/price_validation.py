from app.schemas.extraction import ExtractionResult
from app.schemas.validation import ValidationResult

from .base_rule import BaseValidationRule


class PriceValidationRule(BaseValidationRule):

    def validate(
        self,
        extraction: ExtractionResult,
        validation: ValidationResult,
    ) -> None:

        if extraction.raw_total is None:
            validation.errors.append(
                "Raw total is missing."
            )
            return

        expected = extraction.raw_total

        if extraction.applied_discount_percentage is not None:
            expected -= (
                extraction.raw_total
                * extraction.applied_discount_percentage
                / 100
            )

        expected = round(expected, 2)

        validation.final_calculated_total = expected

        # لو الفاتورة نفسها فيها Final Total
        if extraction.invoice_final_total is not None:

            validation.price_calculation_valid = (
                abs(
                    expected
                    - extraction.invoice_final_total
                )
                < 0.01
            )

            if not validation.price_calculation_valid:

                validation.errors.append(
                    "Price calculation mismatch."
                )

        else:
            # مفيش قيمة نقارن بيها
            validation.warnings.append(
                "Invoice final total not provided."
            )

            validation.price_calculation_valid = True