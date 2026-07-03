from pathlib import Path

from app.infrastructure.parsers.strategies.pdf_parser import PDFParser
from app.infrastructure.parsers.strategies.docx_parser import DOCXParser
from app.infrastructure.parsers.strategies.image_parser import ImageParser


class ParserFactory:

    @staticmethod
    def create(file_path: str):
        extension = Path(file_path).suffix.lower()

        if extension == ".pdf":
            return PDFParser()

        if extension == ".docx":
            return DOCXParser()

        if extension in [".png", ".jpg", ".jpeg"]:
            return ImageParser()

        raise ValueError(f"Unsupported file type: {extension}")