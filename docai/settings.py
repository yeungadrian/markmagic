"""Settings for markdown conversion."""

from pydantic import BaseModel, field_validator
from tabulate import tabulate_formats


class TableSettings(BaseModel):
    """Table format settings."""

    # Dynamic list to sync with tabulate
    tablefmt: str = "github"
    showindex: bool = True
    headers: str = "firstrow"

    @field_validator("tablefmt")
    def validate_tablefmt(cls, v: str) -> str:
        """Validate tablefmt."""
        assert v in tabulate_formats
        return v


class Settings(BaseModel):
    """DocAI Settings."""

    tables: TableSettings = TableSettings()
