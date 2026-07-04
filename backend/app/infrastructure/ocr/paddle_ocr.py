"""
PaddleOCR Engine
================

Lazy-loaded singleton for PaddleOCR.

The OCR engine is created only on the first request and then cached for
the lifetime of the application.

This keeps application startup fast while avoiding repeated model loading.
"""

from functools import lru_cache


@lru_cache(maxsize=1)
def get_ocr_engine():
    """
    Return a cached PaddleOCR instance.

    Raises:
        ImportError:
            If PaddleOCR is not installed.

        RuntimeError:
            If the OCR engine cannot be initialized.
    """

    try:
        from paddleocr import PaddleOCR
    except ImportError as exc:
        raise ImportError(
            "PaddleOCR is not installed. "
            "Install it with:\n"
            "pip install paddlepaddle paddleocr"
        ) from exc

    try:
        return PaddleOCR(
            use_doc_orientation_classify=False,
            use_doc_unwarping=False,
            use_textline_orientation=False,
        )
    except Exception as exc:
        raise RuntimeError(
            "Failed to initialize PaddleOCR. "
            "This is usually caused by incompatible versions of "
            "paddlepaddle, paddleocr, or paddlex."
        ) from exc