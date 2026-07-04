"""
PaddleOCR Engine — lazy initialisation
========================================
PaddleOCR is a heavy optional dependency (requires C++ tooling and GPU drivers).
We avoid importing it at module-load time so the rest of the application can
start without it installed.

The engine is instantiated on first call to `get_ocr_engine()`.
"""

_ocr_engine = None


def get_ocr_engine():
    """Return the shared PaddleOCR instance, initialising it on first call."""
    global _ocr_engine
    if _ocr_engine is None:
        try:
            from paddleocr import PaddleOCR  # noqa: PLC0415
        except ImportError as exc:
            raise ImportError(
                "PaddleOCR is not installed. "
                "Install it with: pip install paddlepaddle paddleocr"
            ) from exc

        _ocr_engine = PaddleOCR(
            use_doc_orientation_classify=True,
            use_doc_unwarping=True,
            use_textline_orientation=True,
        )
    return _ocr_engine