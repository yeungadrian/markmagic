from pydantic import BaseModel


class Chunk(BaseModel):
    """Single section from converted document."""

    content: str
    table: bool | None = False
    n_tokens: int = 0
    chunked: bool | None = None


class MetaData(BaseModel):
    """Shared metadata."""

    filename: str
    sheet_name: str | None = None


class PartitionedDocument(BaseModel):
    """Document model."""

    chunks: list[Chunk]
    metadata: MetaData


class DocumentMetaData(BaseModel):
    """Metadata for vectorstore."""

    filename: str
    sheet_name: str | None = None
    table: bool | None = False
    estimated_tokens: int
    overlap_start: int | None = None


class Document(BaseModel):
    """Document ready for vectorstore."""

    content: str
    metadata: DocumentMetaData
