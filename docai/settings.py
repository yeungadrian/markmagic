"""Settings for markdown conversion."""

from typing import Literal

from pydantic import BaseModel
from tabulate import tabulate_formats


class TableSettings(BaseModel):
    """Table format settings."""

    # Dynamic list to sync with tabulate
    tablefmt: Literal[*tabulate_formats] = "github"  # type: ignore[valid-type]
    showindex: bool = True
    headers: str = "firstrow"


class Settings(BaseModel):
    """DocAI Settings."""

    tables: TableSettings = TableSettings()
