"""
GPTOSSExtractor
===============
LLM extraction strategy using the OpenAI-compatible GPT-OSS endpoint.

Uses PromptBuilder to construct the structured prompt and `beta.chat.completions.parse`
for typed response parsing into ExtractionResult.
"""

from app.infrastructure.extraction.builders.prompt_builder import PromptBuilder
from app.infrastructure.extraction.groq_client import groq_client
from app.schemas.attachment import Attachment
from app.schemas.extraction import ExtractionResult

from .base_extractor import BaseExtractor


class GPTOSSExtractor(BaseExtractor):

    GPT_OSS_MODEL = "openai/gpt-oss-120b"

    async def extract(
        self,
        subject: str,
        body: str,
        attachments: list[Attachment],
    ) -> ExtractionResult:

        messages = (
            PromptBuilder()
            .add_email(subject, body)
            .add_documents(attachments)
            .add_schema(ExtractionResult.model_json_schema())
            .build()
        )

        response = await groq_client.beta.chat.completions.parse(
            model=self.GPT_OSS_MODEL,
            messages=messages,
            response_format=ExtractionResult,
        )

        return response.choices[0].message.parsed
