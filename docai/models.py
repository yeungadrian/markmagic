from pydantic import BaseModel


class Chunk(BaseModel):
    """Single section from converted document."""

    content: str
    table: bool | None = False
    n_tokens: int = 0
    chunked: bool | None = False


class MetaData(BaseModel):
    """File metadata."""

    filename: str
    sheet_name: str | None = None


class PartitionedDocument(BaseModel):
    """Partitioned document model."""

    chunks: list[Chunk]
    metadata: MetaData


class DocumentMetaData(BaseModel):
    """Metadata for single document vectorstore."""

    filename: str
    sheet_name: str | None = None
    table: bool | None = False
    estimated_tokens: int
    overlap_start: int | None = None


class Document(BaseModel):
    """Document ready for vectorstore."""

    content: str
    metadata: DocumentMetaData
