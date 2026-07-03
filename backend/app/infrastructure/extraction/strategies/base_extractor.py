from abc import ABC, abstractmethod

from app.schemas.attachment import Attachment
from app.schemas.extraction import ExtractionResult


class BaseExtractor(ABC):

    @abstractmethod
    async def extract(
        self,
        subject: str,
        body: str,
        attachments: list[Attachment],
    ) -> ExtractionResult:
        """
        Extract structured business information.
        """
        ...