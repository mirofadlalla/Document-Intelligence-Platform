from enum import Enum

from pydantic import BaseModel


class AttachmentType(str, Enum):
    PDF = "pdf"
    DOCX = "docx"
    IMAGE = "image"


class Attachment(BaseModel):
    filename: str
    file_type: AttachmentType

    # Original uploaded file location
    file_path: str

    # Output of the parser/OCR
    extracted_text: str | None = None

# ه أضفنا file_path؟
# تخيل بعد شوية هنعمل
# attachments = [
#     Attachment(...),
#     Attachment(...)
# ]

# بعد الـ Parsing هيبقوا
# Attachment(
#     filename="invoice.pdf",
#     file_type=AttachmentType.PDF,
#     file_path="/uploads/invoice.pdf",
#     extracted_text="Invoice No: INV-1001..."
# )

# وبعدها الـ LLM هيستقبل
# for attachment in attachments:
#     attachment.extracted_text

# وبعدها الـ Validation لو حصل Error هيقول
#  Validation failed in invoice.pdf

# بدل ما يقول
# Validation failed

# ومتعرفش فى أنهى ملف.