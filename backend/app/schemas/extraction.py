from pydantic import BaseModel


class FinancialData(BaseModel):

    subtotal: float | None = None

    tax: float | None = None

    discount_percentage: float | None = None

    total: float | None = None


class ExtractionResult(BaseModel):

    vendor_name: str | None = None

    invoice_number: str | None = None

    raw_total: float | None = None

    applied_discount_percentage: float | None = None

    final_calculated_total: float | None = None