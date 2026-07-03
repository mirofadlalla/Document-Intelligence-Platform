from pydantic import BaseModel, Field


class LineItem(BaseModel):
    product_name: str
    quantity: int
    unit_price: float | None = None
    item_code: str | None = None  # Optional: used as primary matching key in CrossDocumentService


class ExtractionResult(BaseModel):

    # Invoice Metadata
    vendor_name: str | None = None
    invoice_number: str | None = None

    # Financial Fields
    raw_total: float | None = None
    applied_discount_percentage: float | None = None
    invoice_final_total: float | None = None

    # Email Hidden Instructions
    is_urgent: bool = False
    routing_instruction: str | None = None

    # Cross Document Tracking
    invoice_line_items: list[LineItem] = Field(default_factory=list)
    delivery_line_items: list[LineItem] = Field(default_factory=list)