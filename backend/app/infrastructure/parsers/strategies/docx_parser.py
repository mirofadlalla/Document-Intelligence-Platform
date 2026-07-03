from docx import Document

from .base_parser import BaseParser


class DOCXParser(BaseParser):

    def parse(self, file_path: str) -> str:
        document = Document(file_path)

        return "\n".join(
            paragraph.text
            for paragraph in document.paragraphs
        )

