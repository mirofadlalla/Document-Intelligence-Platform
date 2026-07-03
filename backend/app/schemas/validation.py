from pydantic import BaseModel, Field


class ValidationResult(BaseModel):

    required_fields_valid: bool = False

    invoice_number_valid: bool = False

    vendor_exists: bool = False

    price_calculation_valid: bool = False

    line_items_match_delivery: bool = False

    final_calculated_total: float | None = None

    confidence_score: float = Field(
        default=0,
        ge=0,
        le=1,
    )

    # errors: list[str] = []

    # warnings: list[str] = []
    
    errors: list[str] = Field(default_factory=list)

    warnings: list[str] = Field(default_factory=list)