# import pytesseract

# from PIL import Image

# from .base_parser import BaseParser


# class ImageParser(BaseParser):

#     def parse(self, file_path: str) -> str:
#         image = Image.open(file_path)

#         return pytesseract.image_to_string(image)


from app.infrastructure.ocr.paddle_ocr import ocr_engine
from .base_parser import BaseParser


class ImageParser(BaseParser):

    def parse(self, file_path: str) -> str:
        result = ocr_engine.predict(file_path)

        texts = []

        for page in result:
            texts.extend(page.get("rec_texts", []))

        return "\n".join(texts)