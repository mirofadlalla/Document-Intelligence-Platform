"""
CrossDocumentService
====================
Deterministic line-item comparator used by DeliveryValidationRule.

Matching Priority
-----------------
1. item_code  — if BOTH items carry a non-empty item_code, compare on that.
2. normalized description — lowercase, strip, collapse multiple spaces.

After a match is found, quantity equality is validated.
"""

import re
from dataclasses import dataclass, field

from app.schemas.extraction import LineItem


@dataclass
class MatchResult:
    """Structured result returned by CrossDocumentService.compare()."""

    matches: bool
    mismatches: list[str] = field(default_factory=list)


def _normalize(text: str) -> str:
    """Lowercase, strip, collapse internal whitespace runs to a single space."""
    return re.sub(r"\s+", " ", text.lower().strip())


class CrossDocumentService:
    """
    Compares invoice line items against delivery line items deterministically.

    Usage::

        service = CrossDocumentService()
        result = service.compare(invoice_items, delivery_items)
        # result.matches -> bool
        # result.mismatches -> list[str]
    """

    def compare(
        self,
        invoice_items: list[LineItem],
        delivery_items: list[LineItem],
    ) -> MatchResult:

        mismatches: list[str] = []

        # Build a lookup map for delivery items.
        # Key: item_code (if present) or normalized product_name.
        delivery_map: dict[str, LineItem] = {}
        for item in delivery_items:
            key = self._item_key(item)
            delivery_map[key] = item

        matched_keys: set[str] = set()

        for inv_item in invoice_items:
            key = self._item_key(inv_item)

            if key not in delivery_map:
                mismatches.append(
                    f"Invoice item '{inv_item.product_name}' not found in delivery."
                )
                continue

            del_item = delivery_map[key]
            matched_keys.add(key)

            if inv_item.quantity != del_item.quantity:
                mismatches.append(
                    f"Quantity mismatch for '{inv_item.product_name}': "
                    f"invoice={inv_item.quantity}, delivery={del_item.quantity}."
                )

        # Report delivery items that were never matched by an invoice item.
        for key, del_item in delivery_map.items():
            if key not in matched_keys:
                mismatches.append(
                    f"Delivery item '{del_item.product_name}' has no matching invoice item."
                )

        return MatchResult(
            matches=len(mismatches) == 0,
            mismatches=mismatches,
        )

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _item_key(item: LineItem) -> str:
        """
        Returns a deterministic lookup key for an item.

        Priority:
        - item_code (if non-empty)
        - normalized product_name
        """
        if item.item_code and item.item_code.strip():
            return item.item_code.strip()
        return _normalize(item.product_name)
