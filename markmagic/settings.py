"""Settings for markdown conversion."""

from typing import Literal

from pydantic import BaseModel, field_validator
from tabulate import tabulate_formats


class EmailSettings(BaseModel):
    """Email conversion settings."""

    process_attachments: bool = True


class ExcelSettings(BaseModel):
    """Excel conversion settings."""

    skip_empty_area: bool = False


class PDFSettings(BaseModel):
    """PDF conversion settings."""

    extraction_mode: Literal["plain", "layout"] = "plain"


class TableSettings(BaseModel):
    """Table conversion settings."""

    tablefmt: str = "github"  # Type checkers do not support unpacking into a Literal
    showindex: bool = False

    @field_validator("tablefmt")
    def validate_tablefmt(cls, v: str) -> str:
        """Validate tablefmt."""
        assert v in tabulate_formats
        return v


class Settings(BaseModel):
    """Markdown conversion settings."""

    email: EmailSettings = EmailSettings()
    excel: ExcelSettings = ExcelSettings()
    pdf: PDFSettings = PDFSettings()
    tables: TableSettings = TableSettings()
