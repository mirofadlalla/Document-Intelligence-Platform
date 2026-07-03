from pydantic import BaseModel

from pydantic import Field

class ValidationResult(BaseModel):

    line_items_match_delivery: bool

    price_calculation_valid: bool

    confidence_score: float

    errors: list[str] = Field(default_factory=list)