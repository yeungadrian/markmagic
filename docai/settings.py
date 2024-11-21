from typing import Literal

from tabulate import tabulate_formats
from pydantic import BaseModel


class TableSettings(BaseModel):
    # TODO: Check unpacking list[str] into Literal is fine
    # Preference to not maintain list in sync with tabulate
    tablefmt: Literal[*tabulate_formats] = "github"  # type: ignore[valid-type]
    showindex: bool = True


class ExcelSettings(BaseModel):
    skip_empty_area: bool = False


class Settings(BaseModel):
    tables: TableSettings = TableSettings()
    excel: ExcelSettings = ExcelSettings()
