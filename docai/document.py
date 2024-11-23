from pydantic import BaseModel


class MetaData(BaseModel):
    """Metadata model."""

    filename: str
    sheet_name: str | None = None


class Document(BaseModel):
    """Document model."""

    content: str
    metadata: MetaData
