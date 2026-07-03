from app.schemas.extraction import ExtractionResult
from app.services.validation.services.validation_service import (
    ValidationService,
)


def test_validation_pipeline():

    extraction = ExtractionResult(

        vendor_name="ABC TECHNOLOGIES LTD.",

        invoice_number="INV-2026-00125",

        raw_total=4300,

        applied_discount_percentage=10,

        invoice_final_total=3870,
    )

    service = ValidationService()

    result = service.validate(extraction)

    print(result)

    assert result.price_calculation_valid
    assert result.final_calculated_total == 3870

# test_validation_pipeline()