"""
ImageParser
===========
Extracts text from image files (.png / .jpg / .jpeg) using PaddleOCR.

PaddleOCR is lazy-loaded via `get_ocr_engine()` — the module is importable
even when PaddleOCR is not installed.  A clear ImportError is raised at
parse-time if the package is missing.
"""

from app.infrastructure.ocr.paddle_ocr import get_ocr_engine
from .base_parser import BaseParser


class ImageParser(BaseParser):

    def parse(self, file_path: str) -> str:
        ocr_engine = get_ocr_engine()
        result = ocr_engine.predict(file_path)

        texts = []
        for page in result:
            texts.extend(page.get("rec_texts", []))

        return "\n".join(texts)