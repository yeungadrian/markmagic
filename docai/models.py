from datetime import date, datetime, time, timedelta

from pydantic import BaseModel


class MetaData(BaseModel):
    """Metadata model."""

    filename: str
    sheet_name: str | None = None
    table: bool | None = False
    raw_table: list[list[int | float | str | bool | time | date | datetime | timedelta]] | None = None


class Chunk(BaseModel):
    """Chunk model."""

    content: str
    metadata: MetaData
    # Properties used while splitting / merging
    estimated_tokens: int = 0
    chunked: bool | None = False
    overlap_start: int | None = None


class Document(BaseModel):
    """Document model."""

    chunks: list[Chunk]
