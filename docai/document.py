from datetime import date, datetime, time, timedelta

from pydantic import BaseModel


class MetaData(BaseModel):
    """Metadata model."""

    filename: str
    sheet_name: str | None = None
    table: bool | None = False
    raw_table: list[list[int | float | str | bool | time | date | datetime | timedelta]] | None = None


class Document(BaseModel):
    """Document model."""

    content: str
    metadata: MetaData
