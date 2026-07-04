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

    # Legacy Financial Fields (kept for backward compatibility)
    raw_total: float | None = None
    applied_discount_percentage: float | None = None
    
    # Real-world Financial Fields
    subtotal: float | None = None
    tax_amount: float | None = None
    shipping_amount: float | None = None
    discount_amount: float | None = None
    other_charges: float | None = None
    
    # Final Total
    invoice_final_total: float | None = None

    # Email Hidden Instructions
    is_urgent: bool = False
    routing_instruction: str | None = None

    # Cross Document Tracking
    invoice_line_items: list[LineItem] = Field(default_factory=list)
    delivery_line_items: list[LineItem] = Field(default_factory=list)