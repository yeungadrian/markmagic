from typing import Literal

from tabulate import tabulate_formats
from pydantic import BaseModel


class TableSettings(BaseModel):
    tablefmt: Literal[*tabulate_formats] = "github"
    showindex: bool = True


class Settings(BaseModel):
    tables: TableSettings = TableSettings()
