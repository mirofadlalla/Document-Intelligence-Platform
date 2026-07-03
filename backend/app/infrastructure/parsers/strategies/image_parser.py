import pytesseract

from PIL import Image

from .base_parser import BaseParser


class ImageParser(BaseParser):

    def parse(self, file_path: str) -> str:
        image = Image.open(file_path)

        return pytesseract.image_to_string(image)