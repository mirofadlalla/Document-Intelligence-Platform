from pydantic import BaseModel


class ValidationResult(BaseModel):

    line_items_match_delivery: bool

    price_calculation_valid: bool

    confidence_score: float

    errors: list[str] = []