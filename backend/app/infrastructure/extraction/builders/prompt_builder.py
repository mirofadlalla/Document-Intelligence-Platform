import json

from app.schemas.attachment import Attachment


SYSTEM_PROMPT = """
You are an information extraction engine.

Your ONLY responsibility is extracting structured information.

You may receive:
- Email
- Invoice
- Delivery Note
- Delivery Slip
- Purchase Order
- Other business documents

Rules:
1. Return ONLY structured JSON.
2. Never perform calculations.
3. Never validate values.
4. Never infer missing values.
5. Unknown scalar values must be null.
6. Unknown lists must be [].
7. Extract invoice_line_items ONLY from invoice documents.
8. Extract delivery_line_items ONLY from delivery notes or delivery slips.
9. Never merge line items across different documents.
10. Preserve product names exactly as written.
11. Preserve quantities exactly.
12. Preserve item codes exactly.
13. Extract financial fields exactly as written.
14. Extract business signals from the email body when present:
   - urgency
   - routing instructions
   - discount information
   - approval requests
15. Ignore marketing text and signatures.
16. Return valid JSON only.
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

        # Build email section
        email_section = ""
        if self.email:
            email_section = f"""==================================================
EMAIL
==================================================

Subject:
{self.email.get('subject', '')}

Body:
{self.email.get('body', '')}

"""

        # Build documents sections
        doc_sections = []
        for i, doc in enumerate(self.documents, 1):
            doc_sections.append(
                f"""==================================================
ATTACHMENT #{i}
==================================================

Filename:
{doc.get('filename', '')}

Type:
{doc.get('type', '')}

Content:
{doc.get('content', '')}
"""
            )

        user_prompt = f"{email_section}{''.join(doc_sections)}Return JSON following this schema:\n\n{json.dumps(self.schema, indent=2)}"

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