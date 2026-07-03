from pydantic import BaseModel

from pydantic import Field

class ValidationResult(BaseModel):

    # Business Validation
    line_items_match_delivery: bool = False
    price_calculation_valid: bool = False

    # Deterministic Calculation
    final_calculated_total: float | None = None

    # Overall
    confidence_score: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
    )

    errors: list[str] = Field(default_factory=list)

    warnings: list[str] = Field(default_factory=list)