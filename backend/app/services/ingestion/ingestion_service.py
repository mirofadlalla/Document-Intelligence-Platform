from pathlib import Path

from app.infrastructure.parsers.factories.parser_factory import ParserFactory


class IngestionService:

    def parse_documents(self, file_paths: list[str]) -> list[str]:

        documents = []

        for path in file_paths:

            parser = ParserFactory.create(path)

            text = parser.parse(path)

            documents.append(text)

        return documents