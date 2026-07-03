from abc import ABC, abstractmethod


class BaseParser(ABC):
    @abstractmethod
    def parse(self, file_path: str) -> str:
        """Extract normalized text from a document."""
        pass