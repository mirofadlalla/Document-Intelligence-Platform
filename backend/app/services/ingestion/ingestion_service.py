from pathlib import Path

from app.infrastructure.parsers.factories.parser_factory import ParserFactory
from app.schemas.attachment import Attachment

from app.utils.file_utils import get_attachment_type
class IngestionService:

    def parse_documents(self, file_paths: list[str]) -> list[Attachment]:

        attachments = []

        for file_path in file_paths:

            parser = ParserFactory.create(file_path)

            extracted_text = parser.parse(file_path)

            attachments.append(
                Attachment(
                    filename=Path(file_path).name,
                    file_type=get_attachment_type(file_path),
                    file_path=file_path,
                    extracted_text=extracted_text,
                )
            )

        return attachments