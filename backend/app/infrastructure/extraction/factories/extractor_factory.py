"""
ExtractorFactory
================
Selects and constructs the LLM extractor strategy based on configuration.

Supported providers (set via `LLM_PROVIDER` env var):
    - "groq"    → GroqExtractor    (default)
    - "gpt-oss" → GPTOSSExtractor

Adding a new provider:
    1. Create a new strategy in infrastructure/extraction/strategies/.
    2. Add a branch here.
"""

from app.core.config import settings
from app.infrastructure.extraction.strategies.groq_extractor import GroqExtractor
from app.infrastructure.extraction.strategies.gpt_oss_extractor import GPTOSSExtractor


class ExtractorFactory:

    @staticmethod
    def create():
        provider = settings.llm_provider.lower()

        if provider == "groq":
            return GroqExtractor()

        if provider == "gpt-oss":
            return GPTOSSExtractor()

        raise ValueError(
            f"Unsupported LLM provider: '{provider}'. "
            "Supported values: 'groq', 'gpt-oss'."
        )