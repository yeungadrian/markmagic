"""Settings for markdown conversion."""

from pydantic import BaseModel, field_validator
from tabulate import tabulate_formats


class TableSettings(BaseModel):
    """Table format settings."""

    tablefmt: str = "github"  # Type checkers do not support unpacking into a Literal
    showindex: bool = False

    @field_validator("tablefmt")
    def validate_tablefmt(cls, v: str) -> str:
        """Validate tablefmt."""
        assert v in tabulate_formats
        return v


class ExcelSettings(BaseModel):
    """Excel settings."""

    skip_empty_area: bool = False


class Settings(BaseModel):
    """DocAI Settings."""

    tables: TableSettings = TableSettings()
    excel: ExcelSettings = ExcelSettings()
