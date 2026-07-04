#!/usr/bin/env python3
"""
Container Smoke Tests
=====================
Executed inside the Docker container to verify all subsystems work correctly.

Tests:
  1. PDF parser — extracts real text from a PDF fixture.
  2. DOCX parser — extracts real text from a DOCX fixture.
  3. PaddleOCR real extraction — runs a genuine OCR pipeline on a small test
     image (generated on-the-fly so no fixture file is required).
  4. Validation pipeline — runs the full ValidationService on a mock
     ExtractionResult.

Run from the /app directory inside the container:

    python tests/smoke_tests.py
"""

import sys
import os
from pathlib import Path

# Ensure /app is importable
sys.path.insert(0, str(Path(__file__).parent.parent))

PASS = "\033[92m[PASS]\033[0m"
FAIL = "\033[91m[FAIL]\033[0m"
INFO = "\033[94m[INFO]\033[0m"

errors: list[str] = []


def _check(label: str, fn):
    try:
        result = fn()
        print(f"{PASS} {label}")
        return result
    except Exception as exc:
        print(f"{FAIL} {label}: {exc}")
        errors.append(label)
        return None


# ─────────────────────────────────────────────────────────────────────────────
# 1. PDF Parser
# ─────────────────────────────────────────────────────────────────────────────
# NOTE: Disabled because binary test assets were removed from version control
# to comply with Hugging Face Spaces deployment restrictions.
# def _test_pdf_parser():
#     from app.infrastructure.parsers.strategies.pdf_parser import PDFParser

#     pdf_path = Path(__file__).parent / "assets" / "invoice.pdf"
#     assert pdf_path.exists(), f"Fixture not found: {pdf_path}"
#     text = PDFParser().parse(str(pdf_path))
#     assert text.strip(), "PDF parser returned empty text"
#     print(f"   {INFO} Extracted {len(text)} chars from {pdf_path.name}")
#     return text

# _check("PDF parser — extracts text from invoice.pdf", _test_pdf_parser)

# ─────────────────────────────────────────────────────────────────────────────
# 2. DOCX Parser
# ─────────────────────────────────────────────────────────────────────────────
# NOTE: Disabled because binary test assets were removed from version control
# to comply with Hugging Face Spaces deployment restrictions.
# def _test_docx_parser():
#     from app.infrastructure.parsers.strategies.docx_parser import DOCXParser

#     docx_path = (
#         Path(__file__).parent / "assets" / "Delivery Note DN-2026-00481.docx"
#     )
#     assert docx_path.exists(), f"Fixture not found: {docx_path}"
#     text = DOCXParser().parse(str(docx_path))
#     assert text.strip(), "DOCX parser returned empty text"
#     print(f"   {INFO} Extracted {len(text)} chars from {docx_path.name}")
#     return text

# _check("DOCX parser — extracts text from delivery note", _test_docx_parser)

# ─────────────────────────────────────────────────────────────────────────────
# 3. PaddleOCR — real extraction (not just import)
# ─────────────────────────────────────────────────────────────────────────────
def _test_paddle_ocr_real_extraction():
    """
    Generates a small PNG with known text via Pillow, then runs the full
    ImageParser → PaddleOCR pipeline and verifies non-empty output.

    This proves OCR works end-to-end inside the container — it is NOT just
    an import test.
    """
    import tempfile
    from PIL import Image, ImageDraw, ImageFont

    # Build a minimal test image with readable text
    img = Image.new("RGB", (400, 100), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    test_phrase = "Invoice 12345 Total 99.99"
    try:
        # Use a real font if available; fall back to default bitmap font
        font = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf", 24)
    except (IOError, OSError):
        font = ImageFont.load_default()
    draw.text((10, 30), test_phrase, fill=(0, 0, 0), font=font)

    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
        tmp_path = tmp.name
        img.save(tmp_path)

    try:
        from app.infrastructure.parsers.strategies.image_parser import ImageParser

        extracted = ImageParser().parse(tmp_path)
        assert extracted.strip(), (
            "PaddleOCR returned empty string — OCR pipeline did not extract any text"
        )
        print(
            f"   {INFO} PaddleOCR extracted: {repr(extracted[:80])}"
            f"{'...' if len(extracted) > 80 else ''}"
        )
    finally:
        os.unlink(tmp_path)

    return extracted


_check(
    "PaddleOCR — real OCR extraction from generated image (not just import)",
    _test_paddle_ocr_real_extraction,
)

# ─────────────────────────────────────────────────────────────────────────────
# 4. Validation Pipeline
# ─────────────────────────────────────────────────────────────────────────────
def _test_validation_pipeline():
    from app.schemas.extraction import ExtractionResult
    from app.services.validation.services.validation_service import ValidationService

    # Construct a minimal ExtractionResult with the fields the validation rules
    # actually inspect (vendor_name, invoice_number, subtotal are required).
    extraction = ExtractionResult(
        invoice_number="INV-2026-00125",
        vendor_name="Acme Corp",
        subtotal=100.0,
        tax_amount=10.0,
        discount_amount=0.0,
        invoice_final_total=110.0,
        is_urgent=False,
        routing_instruction=None,
    )

    svc = ValidationService()
    result = svc.validate(extraction)
    assert result is not None, "ValidationService returned None"
    assert 0.0 <= result.confidence_score <= 1.0, (
        f"confidence_score out of range: {result.confidence_score}"
    )
    print(
        f"   {INFO} Validation complete — confidence={result.confidence_score}, "
        f"errors={result.errors}, warnings={result.warnings}"
    )
    return result



_check("Validation pipeline — runs all rules on mock ExtractionResult", _test_validation_pipeline)

# ─────────────────────────────────────────────────────────────────────────────
# 5. Health endpoint (import-level check)
# ─────────────────────────────────────────────────────────────────────────────
def _test_health_route():
    from app.api.routes.health import health_check
    import asyncio

    result = asyncio.run(health_check())
    assert result.get("status") == "healthy", f"Unexpected health response: {result}"
    return result


_check("Health endpoint — returns {status: healthy}", _test_health_route)

# ─────────────────────────────────────────────────────────────────────────────
# Summary
# ─────────────────────────────────────────────────────────────────────────────
print()
if errors:
    print(f"{FAIL} {len(errors)} smoke test(s) failed: {', '.join(errors)}")
    sys.exit(1)
else:
    print(f"{PASS} All smoke tests passed.")
    sys.exit(0)
