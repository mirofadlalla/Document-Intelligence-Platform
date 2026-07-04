import logging
import os


def _get_log_level() -> int:
    """Read LOG_LEVEL from environment, default INFO."""
    level_name = os.getenv("LOG_LEVEL", "INFO").upper()
    return getattr(logging, level_name, logging.INFO)


logging.basicConfig(
    level=_get_log_level(),
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

logger = logging.getLogger("document_intelligence")