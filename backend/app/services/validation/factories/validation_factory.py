from app.services.validation.rules.delivery_validation import (
    DeliveryValidationRule,
)
from app.services.validation.rules.invoice_validation import (
    InvoiceValidationRule,
)
from app.services.validation.rules.price_validation import (
    PriceValidationRule,
)


class ValidationFactory:

    @staticmethod
    def create():

        return [

            InvoiceValidationRule(),

            PriceValidationRule(),

            DeliveryValidationRule(),

        ]