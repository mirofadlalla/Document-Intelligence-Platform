from app.core.config import settings
from app.infrastructure.extraction.builders.prompt_builder import PromptBuilder
from app.infrastructure.extraction.clients.groq_client import groq_client
from app.infrastructure.extraction.providers.base_extractor import BaseExtractor
from app.schemas.attachment import Attachment
from app.schemas.extraction import ExtractionResult


class GroqExtractor(BaseExtractor):

    def __init__(self):

        self.client = groq_client
        self.model = settings.llm_model

    async def extract(
        self,
        subject: str,
        body: str,
        attachments: list[Attachment],
    ) -> ExtractionResult:

        messages = PromptBuilder().build(
            subject=subject,
            body=body,
            attachments=attachments,
        )

        response = await self.client.beta.chat.completions.parse(
            model=self.model,
            messages=messages,
            response_format=ExtractionResult,
        )

        return response.choices[0].message.parsed