from app.schemas.extraction import ExtractionResult
from app.schemas.validation import ValidationResult

from app.services.validation.factories.validation_factory import (
    ValidationFactory,
)


class ValidationService:

    def __init__(self):

        self.rules = ValidationFactory.create()

    def validate(
        self,
        extraction: ExtractionResult,
    ) -> ValidationResult:

        validation = ValidationResult()

        for rule in self.rules:

            rule.validate(
                extraction,
                validation,
            )

        passed = 0
        total = 3

        if validation.price_calculation_valid:
            passed += 1

        if validation.line_items_match_delivery:
            passed += 1

        if len(validation.errors) == 0:
            passed += 1

        validation.confidence_score = round(
            passed / total,
            2,
        )

        return validation