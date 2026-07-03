from pydantic import BaseModel

from app.schemas.attachment import Attachment


class Email(BaseModel):

    sender: str

    subject: str

    body: str

    attachments: list[Attachment]