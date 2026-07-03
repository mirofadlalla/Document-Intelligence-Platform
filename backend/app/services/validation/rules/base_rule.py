from abc import ABC, abstractmethod

from app.schemas.extraction import ExtractionResult
from app.schemas.validation import ValidationResult


class BaseValidationRule(ABC):

    @abstractmethod
    def validate(
        self,
        extraction: ExtractionResult,
        validation: ValidationResult,
    ) -> None:
        """
        Mutates ValidationResult in-place.
         الـ Rule بتعدل على الـ ValidationResult مباشرة.

        مش بترجع Object جديد كل مرة.
        """
        ...