import json

from app.schemas.attachment import Attachment


def _classify_document(filename: str, content: str | None) -> str:
    """
    Infer the business document type from the filename and a snippet of the
    document content. Returns a human-readable label that is embedded in the
    prompt so the LLM knows which documents are invoices and which are delivery
    notes — without relying on file-format type alone.
    """
    name_lower = filename.lower()
    snippet = (content or "")[:500].lower()

    # Delivery note / slip signals
    delivery_keywords = [
        "delivery note", "delivery slip", "delivery order",
        "despatch note", "dispatch note",
        "dn-", "dn ",
    ]
    if any(kw in name_lower or kw in snippet for kw in delivery_keywords):
        return "Delivery Note / Delivery Slip"

    # Invoice signals
    invoice_keywords = [
        "invoice", "inv-", "bill ", "billing",
        "tax invoice", "proforma",
    ]
    if any(kw in name_lower or kw in snippet for kw in invoice_keywords):
        return "Invoice"

    # Purchase order signals
    po_keywords = ["purchase order", "po-", "po ", "order form"]
    if any(kw in name_lower or kw in snippet for kw in po_keywords):
        return "Purchase Order"

    return "Unknown Business Document"


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
7. Extract invoice_line_items ONLY from documents labeled "Document Type: Invoice".
8. Extract delivery_line_items ONLY from documents labeled "Document Type: Delivery Note / Delivery Slip".
9. IMPORTANT: It is normal and REQUIRED that invoice_line_items and delivery_line_items contain
   the same items. Extract them independently from their respective source documents.
   Do NOT leave delivery_line_items empty just because the items also appear in the invoice.
10. Never merge line items across different documents.
11. Preserve product names exactly as written.
12. Preserve quantities exactly.
13. Preserve item codes exactly.
14. Extract financial fields exactly as written.
15. Extract business signals from the email body when present:
   - urgency
   - routing instructions
   - discount information
   - approval requests
16. Ignore marketing text and signatures.
17. Return valid JSON only.
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
                "file_format": attachment.file_type.value,
                "document_type": _classify_document(
                    attachment.filename, attachment.extracted_text
                ),
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

Document Type:
{doc.get('document_type', '')}

File Format:
{doc.get('file_format', '')}

Content:
{doc.get('content', '')}
"""
            )

        # Build a document map summary at the top so the LLM sees
        # the classified types before reading each document.
        doc_map_lines = []
        for i, doc in enumerate(self.documents, 1):
            doc_map_lines.append(
                f"  Attachment #{i}: {doc.get('filename', '')} "
                f"→ {doc.get('document_type', 'Unknown')}"
            )
        doc_map_section = ""
        if doc_map_lines:
            doc_map_section = (
                "DOCUMENT MAP\n"
                + "=" * 50 + "\n"
                + "\n".join(doc_map_lines)
                + "\n\n"
            )

        user_prompt = f"{email_section}{doc_map_section}{''.join(doc_sections)}Return JSON following this schema:\n\n{json.dumps(self.schema, indent=2)}"

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