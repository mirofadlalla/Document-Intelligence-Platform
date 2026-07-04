"""
ParserFactory
=============
Selects the correct parser strategy for a given file extension.

Supported types:
    .pdf   → PDFParser   (pdfplumber)
    .docx  → DOCXParser  (python-docx)
    .png   → ImageParser (PaddleOCR)
    .jpg   → ImageParser
    .jpeg  → ImageParser
"""

from pathlib import Path

from app.core.constants import SUPPORTED_EXTENSIONS
from app.infrastructure.parsers.strategies.docx_parser import DOCXParser
from app.infrastructure.parsers.strategies.image_parser import ImageParser
from app.infrastructure.parsers.strategies.pdf_parser import PDFParser


class ParserFactory:

    @staticmethod
    def create(file_path: str):
        extension = Path(file_path).suffix.lower()

        if extension not in SUPPORTED_EXTENSIONS:
            raise ValueError(f"Unsupported file type: {extension}")

        if extension == ".pdf":
            return PDFParser()

        if extension == ".docx":
            return DOCXParser()

        if extension in {".png", ".jpg", ".jpeg"}:
            return ImageParser()

        raise ValueError(f"Unsupported file type: {extension}")