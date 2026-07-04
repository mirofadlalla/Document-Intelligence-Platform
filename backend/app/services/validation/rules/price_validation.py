from app.schemas.extraction import ExtractionResult
from app.schemas.validation import ValidationResult

from .base_rule import BaseValidationRule


class PriceValidationRule(BaseValidationRule):

    def validate(
        self,
        extraction: ExtractionResult,
        validation: ValidationResult,
    ) -> None:

        # Step 1: Calculate subtotal
        subtotal = 0.0
        if extraction.subtotal is not None:
            subtotal = extraction.subtotal
        elif extraction.raw_total is not None:
            subtotal = extraction.raw_total
        elif extraction.invoice_line_items:
            # Fallback to summing up line items
            subtotal = sum(
                item.quantity * item.unit_price
                for item in extraction.invoice_line_items
                if item.quantity is not None and item.unit_price is not None
            )

        # Step 2: Extract other components (default to 0.0 if missing)
        tax = extraction.tax_amount or 0.0
        shipping = extraction.shipping_amount or 0.0
        other = extraction.other_charges or 0.0

        # Step 3: Calculate discount
        discount = 0.0
        if extraction.discount_amount is not None:
            discount = extraction.discount_amount
        elif extraction.applied_discount_percentage is not None:
            discount = subtotal * (extraction.applied_discount_percentage / 100)

        # Step 4: Calculate expected total
        expected = subtotal + tax + shipping + other - discount
        expected = round(expected, 2)
        validation.final_calculated_total = expected

        # Step 5: Validation Comparison
        if extraction.invoice_final_total is not None:
            diff = abs(expected - extraction.invoice_final_total)
            validation.price_calculation_valid = diff <= 0.01

            if not validation.price_calculation_valid:
                validation.errors.append(
                    f"Price calculation mismatch. "
                    f"Expected: {expected:.2f}, Extracted: {extraction.invoice_final_total:.2f}. Diff: {diff:.2f}. "
                    f"Components used: Subtotal: {subtotal:.2f}, Tax: {tax:.2f}, "
                    f"Shipping: {shipping:.2f}, Other: {other:.2f}, Discount: {discount:.2f}"
                )
        else:
            validation.warnings.append("Invoice final total not provided.")
            validation.price_calculation_valid = True