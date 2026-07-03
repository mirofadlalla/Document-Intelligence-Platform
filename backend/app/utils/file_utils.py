from pathlib import Path

from app.schemas.attachment import AttachmentType


def get_attachment_type(file_path: str) -> AttachmentType:
    extension = Path(file_path).suffix.lower()

    if extension == ".pdf":
        return AttachmentType.PDF

    if extension == ".docx":
        return AttachmentType.DOCX

    if extension in {".png", ".jpg", ".jpeg"}:
        return AttachmentType.IMAGE

    raise ValueError(f"Unsupported file type: {extension}")