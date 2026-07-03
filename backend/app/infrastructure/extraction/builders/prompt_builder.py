import json

from app.schemas.attachment import Attachment


SYSTEM_PROMPT = """
You are an information extraction engine.

Extract business information from the provided email and document contents.

Rules:
- Return ONLY structured data.
- Do not perform calculations.
- Do not validate values.
- Do not infer missing values.
- Leave unknown fields as null.
"""


class PromptBuilder:

    def __init__(self):
        self.email = {}
        self.documents = []
        self.schema = {}

    def add_email(self, subject: str, body: str):
        self.email = {
            "subject": subject,
            "body": body,
        }
        return self

    def add_documents(self, attachments: list[Attachment]):
        self.documents = [
            {
                "filename": attachment.filename,
                "type": attachment.file_type.value,
                "content": attachment.extracted_text,
            }
            for attachment in attachments
        ]
        return self

    def add_schema(self, schema: dict):
        self.schema = schema
        return self

    def build(self):

        user_prompt = f"""
Email

{json.dumps(self.email, indent=2)}

Documents

{json.dumps(self.documents, indent=2)}

Return JSON following this schema:

{json.dumps(self.schema, indent=2)}
"""

        return [
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ]