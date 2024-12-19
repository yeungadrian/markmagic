"""Settings for markdown conversion."""

from pydantic import BaseModel, field_validator
from tabulate import tabulate_formats


class TableSettings(BaseModel):
    """Table format settings."""

    tablefmt: str = "github"
    showindex: bool = False

    @field_validator("tablefmt")
    def validate_tablefmt(cls, v: str) -> str:
        """Validate tablefmt."""
        assert v in tabulate_formats
        return v


class Settings(BaseModel):
    """DocAI Settings."""

    tables: TableSettings = TableSettings()
