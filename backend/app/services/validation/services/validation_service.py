"""
ValidationService
==================
Orchestrates all validation rules and produces a complete ValidationResult.

Responsibilities
----------------
1. Run each rule in order (rules mutate ValidationResult in-place).
2. Convert extraction business signals into deterministic warnings:
       is_urgent            → "Urgent processing requested."
       routing_instruction  → "Manual routing instruction detected."
   This keeps WorkflowService completely decoupled from ExtractionResult.
3. Calculate a dynamic confidence score:
       score = passed_checks / total_checks   (range 0.0 – 1.0)
   The five boolean fields on ValidationResult each count as one check.
"""

from app.schemas.extraction import ExtractionResult
from app.schemas.validation import ValidationResult

from app.services.validation.factories.validation_factory import (
    ValidationFactory,
)


class ValidationService:

    # The 5 boolean flags that each contribute equally to confidence.
    _CONFIDENCE_FLAGS: list[str] = [
        "required_fields_valid",
        "invoice_number_valid",
        "vendor_exists",
        "price_calculation_valid",
        "line_items_match_delivery",
    ]

    def __init__(self):
        self.rules = ValidationFactory.create()

    def validate(
        self,
        extraction: ExtractionResult,
    ) -> ValidationResult:

        validation = ValidationResult()

        # ------------------------------------------------------------------ #
        # 1. Run all deterministic validation rules                           #
        # ------------------------------------------------------------------ #
        for rule in self.rules:
            rule.validate(extraction, validation)

        # ------------------------------------------------------------------ #
        # 2. Convert extraction business signals into validation warnings     #
        #    WorkflowService only ever inspects errors / warnings — it never  #
        #    receives ExtractionResult directly.                              #
        # ------------------------------------------------------------------ #
        if extraction.is_urgent:
            validation.warnings.append("Urgent processing requested.")

        if extraction.routing_instruction:
            validation.warnings.append(
                f"Manual routing instruction detected: "
                f"'{extraction.routing_instruction}'."
            )

        # ------------------------------------------------------------------ #
        # 3. Dynamic confidence score                                         #
        # ------------------------------------------------------------------ #
        total_checks = len(self._CONFIDENCE_FLAGS)

        passed_checks = sum(
            1
            for flag in self._CONFIDENCE_FLAGS
            if getattr(validation, flag, False)
        )

        validation.confidence_score = round(
            passed_checks / total_checks,
            2,
        )

        return validation