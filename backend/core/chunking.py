from dataclasses import dataclass
from typing import List

from core.models import LoadedDocument


@dataclass
class DocumentChunk:
    """
    Represents a chunk of text extracted from a document.
    """
    chunk_id: int
    page_number: int
    text: str
    source: str


class TextChunker:
    """
    Splits document pages into overlapping chunks.
    """

    def __init__(self, chunk_size: int = 500, overlap: int = 100):

        if overlap >= chunk_size:
            raise ValueError("overlap must be smaller than chunk_size")

        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk_document(self, document: LoadedDocument) -> List[DocumentChunk]:

        chunks = []
        chunk_id = 1

        for page in document.pages:

            text = page.text.strip()

            if not text:
                continue

            start = 0

            while start < len(text):

                end = start + self.chunk_size

                chunk_text = text[start:end]

                chunks.append(
                    DocumentChunk(
                        chunk_id=chunk_id,
                        page_number=page.page_number,
                        text=chunk_text,
                        source=document.filename,
                    )
                )

                chunk_id += 1

                start += self.chunk_size - self.overlap

        return chunks