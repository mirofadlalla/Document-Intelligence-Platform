from app.core.config import settings

from app.infrastructure.extraction.providers.groq_extractor import (
    GroqExtractor,
)


class ExtractorFactory:

    @staticmethod
    def create():

        provider = settings.llm_provider.lower()

        if provider == "groq":
            return GroqExtractor()

        raise ValueError(
            f"Unsupported provider: {provider}"
        )