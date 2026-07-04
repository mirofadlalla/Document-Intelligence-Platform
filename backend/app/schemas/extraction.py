from pydantic import BaseModel, Field


class LineItem(BaseModel):
    product_name: str = Field(
        description="Product/service name exactly as it appears on the document"
    )
    quantity: int = Field(description="Quantity of the item as an integer")
    unit_price: float | None = Field(
        default=None, description="Unit price if present on the document"
    )
    item_code: str | None = Field(
        default=None,
        description="Item/SKU/product code if present. Used as primary matching key for cross-document validation.",
    )


class ExtractionResult(BaseModel):

    # Invoice Metadata
    vendor_name: str | None = Field(
        default=None, description="Supplier/vendor company name from the invoice"
    )
    invoice_number: str | None = Field(
        default=None, description="Invoice identifier/number from the invoice"
    )

    # Legacy Financial Fields (kept for backward compatibility)
    raw_total: float | None = Field(
        default=None,
        description="Legacy field: original total amount extracted before new schema",
    )
    applied_discount_percentage: float | None = Field(
        default=None,
        description="Legacy field: discount percentage applied to the total",
    )

    # Real-world Financial Fields
    subtotal: float | None = Field(
        default=None,
        description="Subtotal before tax, discounts, and shipping. Usually labeled 'Subtotal', 'Net Amount', or 'Total before tax'.",
    )
    tax_amount: float | None = Field(
        default=None,
        description="Tax/VAT/GST amount. Usually labeled 'Tax', 'VAT', 'GST', or 'Sales Tax'.",
    )
    shipping_amount: float | None = Field(
        default=None,
        description="Shipping/freight/delivery charges. Usually labeled 'Shipping', 'Freight', 'Delivery', or 'Handling'.",
    )
    discount_amount: float | None = Field(
        default=None,
        description="Monetary discount amount deducted from subtotal. Usually labeled 'Discount', 'Early Payment Discount', or 'Trade Discount'.",
    )
    other_charges: float | None = Field(
        default=None,
        description="Any other charges not covered above (e.g., fees, surcharges).",
    )

    # Final Total
    invoice_final_total: float | None = Field(
        default=None,
        description="Final amount payable. Usually labeled 'Total', 'Grand Total', 'Amount Due', 'Invoice Total', or 'Balance Due'.",
    )

    # Email Hidden Instructions (Business Signals)
    is_urgent: bool = Field(
        default=False,
        description="True if email indicates urgency (e.g., 'urgent', 'asap', 'immediate', 'rush', 'priority', 'expedite').",
    )
    routing_instruction: str | None = Field(
        default=None,
        description="Explicit routing/approval instruction from email body (e.g., 'send to finance', 'route to manager', 'needs approval', 'forward to accounting', 'send for review').",
    )

    # Cross Document Tracking
    invoice_line_items: list[LineItem] = Field(
        default_factory=list,
        description="Line items extracted ONLY from invoice documents. Each item must preserve product_name, quantity, unit_price, and item_code exactly as written.",
    )
    delivery_line_items: list[LineItem] = Field(
        default_factory=list,
        description=(
            "Line items extracted ONLY from delivery note or delivery slip documents. "
            "IMPORTANT: Even if these items also appear in the invoice, you MUST extract "
            "them here independently from the delivery document. "
            "This list should NOT be empty when a delivery note is present. "
            "Each item must preserve product_name, quantity, unit_price, and item_code exactly as written."
        ),
    )