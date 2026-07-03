from enum import Enum

from pydantic import BaseModel


class AttachmentType(str, Enum):

    PDF = "pdf"

    DOCX = "docx"

    IMAGE = "image"


class Attachment(BaseModel):

    filename: str

    file_type: AttachmentType

    extracted_text: str | None = None