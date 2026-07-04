"""
Deterministic Validation & Workflow Pipeline Tests
====================================================

All tests are fully deterministic — no LLM calls, no network, no IO.
Each test constructs an ExtractionResult directly, runs the full
ValidationService → WorkflowService pipeline, and asserts the
expected WorkflowAction.

Test matrix:
    1. Successful processing                         → APPROVE
    2. Delivery quantity mismatch                    → ROUTE_TO_HUMAN_REVIEW
    3. Invalid invoice number format                 → REJECT
    4. Discount > 100                                → REJECT
    5. Unknown vendor                                → ROUTE_TO_HUMAN_REVIEW
    6. Corrupted document (all required fields missing) → REJECT
    7. Urgent business instruction (is_urgent=True)  → ROUTE_TO_HUMAN_REVIEW
"""

import pytest

from app.schemas.extraction import ExtractionResult, LineItem
from app.schemas.workflow import WorkflowAction

from app.services.validation.services.validation_service import ValidationService
from app.services.workflow.workflow_service import WorkflowService
from app.pipeline.final_output_builder import FinalOutputBuilder


# ---------------------------------------------------------------------------
# Shared test helpers
# ---------------------------------------------------------------------------

def _run_pipeline(extraction: ExtractionResult) -> WorkflowAction:
    """
    Runs the full ValidationService → WorkflowService pipeline and
    returns the WorkflowAction enum value.
    """
    validation_service = ValidationService()
    workflow_service = WorkflowService()

    validation = validation_service.validate(extraction)
    result = workflow_service.decide(validation)
    return result.action


# ---------------------------------------------------------------------------
# Test 1 — Successful processing → APPROVE
# ---------------------------------------------------------------------------

def test_approve_on_valid_document():
    """
    All fields present, valid format, known vendor, correct discount math,
    matching line items.  Expect: APPROVE.
    """
    extraction = ExtractionResult(
        vendor_name="ABC TECHNOLOGIES LTD.",
        invoice_number="INV-2026-00125",
        raw_total=4300.00,
        applied_discount_percentage=10.0,
        invoice_final_total=3870.00,
        is_urgent=False,
        routing_instruction=None,
        invoice_line_items=[
            LineItem(product_name="Widget A", quantity=5, unit_price=100.0),
            LineItem(product_name="Widget B", quantity=10, unit_price=280.0),
        ],
        delivery_line_items=[
            LineItem(product_name="Widget A", quantity=5),
            LineItem(product_name="Widget B", quantity=10),
        ],
    )

    action = _run_pipeline(extraction)

    assert action == WorkflowAction.APPROVE


# ---------------------------------------------------------------------------
# Test 2 — Delivery quantity mismatch → ROUTE_TO_HUMAN_REVIEW
# ---------------------------------------------------------------------------

def test_route_to_review_on_delivery_mismatch():
    """
    All fields valid, but delivery quantity differs from invoice quantity.
    Expect: ROUTE_TO_HUMAN_REVIEW (mismatch becomes a warning).
    """
    extraction = ExtractionResult(
        vendor_name="ABC TECHNOLOGIES LTD.",
        invoice_number="INV-2026-00200",
        raw_total=1000.00,
        applied_discount_percentage=0.0,
        invoice_final_total=1000.00,
        invoice_line_items=[
            LineItem(product_name="Steel Pipe", quantity=50),
        ],
        delivery_line_items=[
            LineItem(product_name="Steel Pipe", quantity=45),  # mismatch
        ],
    )

    action = _run_pipeline(extraction)

    assert action == WorkflowAction.REVIEW


# ---------------------------------------------------------------------------
# Test 3 — Invalid invoice number → REJECT
# ---------------------------------------------------------------------------

def test_reject_on_invalid_invoice_format():
    """
    Invoice number does not match INV-YYYY-NNNNN pattern.
    Expect: REJECT.
    """
    extraction = ExtractionResult(
        vendor_name="ABC TECHNOLOGIES LTD.",
        invoice_number="2026-INVOICE-001",  # bad format
        raw_total=500.00,
        invoice_final_total=500.00,
    )

    action = _run_pipeline(extraction)

    assert action == WorkflowAction.REJECT


# ---------------------------------------------------------------------------
# Test 4 — Discount > 100 → REJECT
# ---------------------------------------------------------------------------

def test_reject_on_invalid_discount():
    """
    Applied discount is 150% — out of legal range.
    Expect: REJECT.
    """
    extraction = ExtractionResult(
        vendor_name="XYZ INDUSTRIES",
        invoice_number="INV-2026-00300",
        raw_total=2000.00,
        applied_discount_percentage=150.0,  # invalid
    )

    action = _run_pipeline(extraction)

    assert action == WorkflowAction.REJECT


# ---------------------------------------------------------------------------
# Test 5 — Unknown vendor → ROUTE_TO_HUMAN_REVIEW
# ---------------------------------------------------------------------------

def test_route_to_review_on_unknown_vendor():
    """
    Vendor not in approved whitelist → warning (not error).
    No other issues.
    Expect: ROUTE_TO_HUMAN_REVIEW.
    """
    extraction = ExtractionResult(
        vendor_name="Acme Corp.",         # not in APPROVED_VENDORS
        invoice_number="INV-2026-00400",
        raw_total=750.00,
        invoice_final_total=750.00,
    )

    action = _run_pipeline(extraction)

    assert action == WorkflowAction.REVIEW


# ---------------------------------------------------------------------------
# Test 6 — Corrupted document (all required fields missing) → REJECT
# ---------------------------------------------------------------------------

def test_reject_on_missing_required_fields():
    """
    Document is completely corrupted — no vendor, no invoice number, no total.
    Expect: REJECT.
    """
    extraction = ExtractionResult(
        vendor_name=None,
        invoice_number=None,
        raw_total=None,
    )

    action = _run_pipeline(extraction)

    assert action == WorkflowAction.REJECT


def test_reject_on_missing_required_fields_sets_errors():
    """
    Supplementary check: ValidationResult.errors should contain messages
    for all three missing fields.
    """
    extraction = ExtractionResult(
        vendor_name=None,
        invoice_number=None,
        raw_total=None,
    )

    validation_service = ValidationService()
    validation = validation_service.validate(extraction)

    # All three required-field errors must be present
    assert not validation.required_fields_valid
    assert any("vendor" in e.lower() for e in validation.errors)
    assert any("invoice number" in e.lower() for e in validation.errors)
    assert any("subtotal" in e.lower() for e in validation.errors)


# ---------------------------------------------------------------------------
# Test 7 — Urgent flag → warning → ROUTE_TO_HUMAN_REVIEW
# ---------------------------------------------------------------------------

def test_route_to_review_on_urgent_flag():
    """
    Extraction contains is_urgent=True (LLM extracted from email body).
    ValidationService converts this into a warning.
    WorkflowService sees the warning and routes to human review.
    Expect: ROUTE_TO_HUMAN_REVIEW.
    """
    extraction = ExtractionResult(
        vendor_name="Global Supplies Ltd.",
        invoice_number="INV-2026-00500",
        raw_total=3200.00,
        invoice_final_total=3200.00,
        is_urgent=True,                  # "URGENT - Please process today."
        routing_instruction=None,
    )

    validation_service = ValidationService()
    workflow_service = WorkflowService()

    validation = validation_service.validate(extraction)
    result = workflow_service.decide(validation)

    # The urgent flag must have been converted into a warning
    assert any("urgent" in w.lower() for w in validation.warnings)

    # WorkflowService must route to human review
    assert result.action == WorkflowAction.REVIEW


# ---------------------------------------------------------------------------
# Test 8 — FinalOutputBuilder integration
# ---------------------------------------------------------------------------

def test_final_output_builder_produces_correct_shape():
    """
    Ensures FinalOutputBuilder fluent API assembles a valid ProcessResponse
    with all required fields correctly set.
    """
    from datetime import datetime, timezone

    extraction = ExtractionResult(
        vendor_name="ABC TECHNOLOGIES LTD.",
        invoice_number="INV-2026-00125",
        raw_total=1000.00,
        invoice_final_total=1000.00,
    )

    validation_service = ValidationService()
    workflow_service = WorkflowService()

    validation = validation_service.validate(extraction)
    workflow_result = workflow_service.decide(validation)

    now = datetime.now(tz=timezone.utc)

    response = (
        FinalOutputBuilder()
        .metadata(source_email="finance@example.com", timestamp_processed=now)
        .extraction(extraction)
        .validation(validation)
        .workflow(workflow_result.action)
        .build()
    )

    assert response.metadata.source_email == "finance@example.com"
    assert response.extraction.invoice_number == "INV-2026-00125"
    assert response.validation.confidence_score >= 0.0
    assert response.workflow_action in list(WorkflowAction)


def test_final_output_builder_raises_on_missing_parts():
    """
    FinalOutputBuilder.build() must raise ValueError when a required
    part is missing.
    """
    import pytest

    with pytest.raises(ValueError, match="missing parts"):
        FinalOutputBuilder().build()


# ---------------------------------------------------------------------------
# Test — Confidence score is calculated dynamically
# ---------------------------------------------------------------------------

def test_confidence_score_is_dynamic():
    """
    A fully valid document should have a higher confidence score
    than one with a missing vendor.
    """
    full = ExtractionResult(
        vendor_name="ABC TECHNOLOGIES LTD.",
        invoice_number="INV-2026-00125",
        raw_total=1000.00,
        invoice_final_total=1000.00,
    )

    partial = ExtractionResult(
        vendor_name="Unknown Corp",  # warning, vendor_exists=False
        invoice_number="INV-2026-00126",
        raw_total=1000.00,
        invoice_final_total=1000.00,
    )

    svc = ValidationService()

    full_score = svc.validate(full).confidence_score
    partial_score = svc.validate(partial).confidence_score

    assert full_score > partial_score
    assert 0.0 <= full_score <= 1.0
    assert 0.0 <= partial_score <= 1.0


# ---------------------------------------------------------------------------
# Test — item_code matching takes priority over product_name
# ---------------------------------------------------------------------------

def test_cross_document_matches_by_item_code_over_name():
    """
    When both sides have item_code, matching uses item_code — even if
    product_name differs (e.g. abbreviation vs full name).
    """
    from app.services.matching.cross_document_service import CrossDocumentService

    service = CrossDocumentService()

    invoice_items = [
        LineItem(product_name="Widget A",     quantity=10, item_code="SKU-001"),
        LineItem(product_name="Widget B",     quantity=5,  item_code="SKU-002"),
    ]

    delivery_items = [
        # Same item_code, different product_name spelling → must still match
        LineItem(product_name="Widget Alpha", quantity=10, item_code="SKU-001"),
        LineItem(product_name="Widget Beta",  quantity=5,  item_code="SKU-002"),
    ]

    result = service.compare(invoice_items, delivery_items)

    assert result.matches is True
    assert len(result.mismatches) == 0


def test_cross_document_detects_quantity_mismatch_via_item_code():
    """
    item_code matches but quantity differs → mismatch reported.
    """
    from app.services.matching.cross_document_service import CrossDocumentService

    service = CrossDocumentService()

    invoice_items = [LineItem(product_name="Part X", quantity=20, item_code="SKU-999")]
    delivery_items = [LineItem(product_name="Part X", quantity=15, item_code="SKU-999")]

    result = service.compare(invoice_items, delivery_items)

    assert result.matches is False
    assert len(result.mismatches) == 1
    assert "SKU-999" in result.mismatches[0] or "Part X" in result.mismatches[0]