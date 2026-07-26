from dataclasses import dataclass, field
from typing import Any


@dataclass
class DocumentPage:
    """
    Represents a single page of a document.
    """

    page_number: int
    text: str


@dataclass
class LoadedDocument:
    """
    Represents an uploaded document.
    """

    filename: str
    file_type: str

    pages: list[DocumentPage]

    metadata: dict[str, Any] = field(default_factory=dict)