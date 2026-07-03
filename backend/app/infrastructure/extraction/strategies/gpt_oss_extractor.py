from app.infrastructure.extraction.builders.prompt_builder import PromptBuilder
from app.infrastructure.extraction.groq_client import client
from app.schemas.extraction import ExtractionResult

from .base_extractor import BaseExtractor


class GPTOSSExtractor(BaseExtractor):

    async def extract(
        self,
        subject: str,
        body: str,
        attachments,
    ) -> ExtractionResult:

        messages = (
            PromptBuilder()
            .add_email(subject, body)
            .add_documents(attachments)
            .add_schema(ExtractionResult.model_json_schema())
            .build()
        )

        response = client.beta.chat.completions.parse(
            model="openai/gpt-oss-120b",
            messages=messages,
            response_format=ExtractionResult,
        )

        return response.choices[0].message.parsed