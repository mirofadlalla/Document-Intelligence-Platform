import json

from app.schemas.attachment import Attachment


def _classify_document(filename: str, content: str | None) -> str:
    """
    Infer the business document type from filename and document content.
    """

    name_lower = filename.lower()
    snippet = (content or "")[:500].lower()

    # Delivery Note
    delivery_keywords = [
        "delivery note",
        "delivery slip",
        "delivery order",
        "dispatch note",
        "despatch note",
        "dn-",
        "dn ",
    ]

    if any(k in name_lower or k in snippet for k in delivery_keywords):
        return "Delivery Note / Delivery Slip"

    # Invoice
    invoice_keywords = [
        "invoice",
        "inv-",
        "tax invoice",
        "proforma",
        "billing",
        "bill ",
    ]

    if any(k in name_lower or k in snippet for k in invoice_keywords):
        return "Invoice"

    # Purchase Order
    po_keywords = [
        "purchase order",
        "po-",
        "po ",
        "order form",
    ]

    if any(k in name_lower or k in snippet for k in po_keywords):
        return "Purchase Order"

    return "Unknown Business Document"


SYSTEM_PROMPT = """
You are an enterprise information extraction engine.

Your ONLY responsibility is extracting structured information.

You may receive:

- Email
- Invoice
- Delivery Note
- Delivery Slip
- Purchase Order
- Other business documents

==========================
GENERAL RULES
==========================

1. Return ONLY valid JSON.
2. Never explain your answer.
3. Never perform calculations.
4. Never validate values.
5. Never infer missing values.
6. Unknown scalar values must be null.
7. Unknown lists must be [].

==========================
DOCUMENT ISOLATION
==========================

8. Treat every attachment as an independent source of truth.

9. Never use information from one attachment
   to complete another attachment.

10. Identify the correct attachment before
    extracting every field.

11. If a field does not exist inside its source
    document, return null.

==========================
INVOICE EXTRACTION
==========================

12. Extract financial fields ONLY from documents
    labeled:

    Document Type: Invoice

13. Financial fields include:

- raw_total
- subtotal
- tax_amount
- shipping_amount
- discount_amount
- other_charges
- applied_discount_percentage
- invoice_final_total

14. Never extract financial fields from:

- Delivery Notes
- Delivery Slips
- Purchase Orders

15. Extract invoice_line_items ONLY from
    Invoice documents.

==========================
DELIVERY EXTRACTION
==========================

16. Extract delivery_line_items ONLY from
    Delivery Note / Delivery Slip documents.

17. invoice_line_items and delivery_line_items
    may legitimately contain the same products.

18. Never merge line items between documents.

19. Preserve exactly:

- product names
- quantities
- unit prices
- item codes

==========================
EMAIL EXTRACTION
==========================

20. Extract the following ONLY from
    the EMAIL BODY:

- urgency
- routing instructions
- approval requests
- discount information

21. Never extract routing instructions
    from invoices or attachments.

==========================
IGNORE
==========================

22. Ignore signatures.

23. Ignore marketing text.

24. Return valid JSON only.
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

        self.documents = []

        for attachment in attachments:
            self.documents.append(
                {
                    "filename": attachment.filename,
                    "file_format": attachment.file_type.value,
                    "document_type": _classify_document(
                        attachment.filename,
                        attachment.extracted_text,
                    ),
                    "content": attachment.extracted_text,
                }
            )

        return self

    def add_schema(self, schema: dict):
        self.schema = schema
        return self

    def build(self):

        email_section = ""

        if self.email:
            email_section = f"""
==================================================
EMAIL
==================================================

Subject:
{self.email.get("subject", "")}

Body:
{self.email.get("body", "")}

"""

        doc_map = []

        for idx, doc in enumerate(self.documents, start=1):
            doc_map.append(
                f"Attachment #{idx}: "
                f"{doc['filename']} "
                f"-> {doc['document_type']}"
            )

        doc_map_section = ""

        if doc_map:
            doc_map_section = (
                "DOCUMENT MAP\n"
                + "=" * 50
                + "\n"
                + "\n".join(doc_map)
                + "\n\n"
            )

        doc_sections = []

        for idx, doc in enumerate(self.documents, start=1):

            doc_sections.append(
                f"""
==================================================
ATTACHMENT #{idx}
==================================================

Filename:
{doc["filename"]}

Document Type:
{doc["document_type"]}

File Format:
{doc["file_format"]}

Document Content:
{doc["content"]}

End Of Attachment.

"""
            )

        user_prompt = (
            email_section
            + doc_map_section
            + "".join(doc_sections)
            + """

IMPORTANT:

Process each attachment independently.

Never use one attachment to complete
another attachment.

Determine the correct source document
for every field before extraction.

If a value does not explicitly exist
inside its source document,
return null.

==================================================

Return JSON using the following schema:

"""
            + json.dumps(self.schema, indent=2)
        )

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