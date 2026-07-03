from pathlib import Path

import pytest

from app.services.ingestion.ingestion_service import IngestionService
from app.infrastructure.extraction.factories.extractor_factory import (
    ExtractorFactory,
)


@pytest.mark.asyncio
async def test_extraction_pipeline():

    ingestion = IngestionService()

    attachments = ingestion.parse_documents(
        [
            str(
                Path(__file__).parent
                / "assets"
                / "invoice.pdf"
            )
        ]
    )

    body = """
Subject:
Invoice INV-2026-00125

Body:

Hello Finance Team,

Please process the attached invoice.

Before approving the payment:

- Apply a 10% discount to the subtotal.
- Validate all totals and taxes.
- Ensure the invoice number matches the document.
- If any required information is missing, send the document for manual review.
- Otherwise, approve the payment.

Thank you.

Best regards,
John Smith
Finance Department
"""

    extractor = ExtractorFactory.create()

    result = await extractor.extract(
        subject="Invoice",
        body=body,
        attachments=attachments,
    )

    print(result)

    assert result is not None



import asyncio

if __name__ == "__main__":
    asyncio.run(test_extraction_pipeline())