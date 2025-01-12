"""Convert excel files to markdown."""

import re
from typing import IO

from python_calamine import CalamineWorkbook
from tabulate import tabulate

from markmagic.settings import Settings


def convert_excel(file: str | IO[bytes], settings: Settings) -> str:
    """Convert excel into markdown."""
    workbook = CalamineWorkbook.from_object(file)  # type: ignore
    markdown = ""
    for sheet_name in workbook.sheet_names:
        calamine_sheet = workbook.get_sheet_by_name(sheet_name)
        tabular_data = calamine_sheet.to_python(skip_empty_area=settings.excel.skip_empty_area)
        tabular_data = [[re.sub(r"\s+", " ", str(j)).strip() for j in i] for i in tabular_data]
        markdown += f"## Sheet: {sheet_name}\n\n"
        markdown += (
            tabulate(
                tabular_data,
                tablefmt=settings.tables.tablefmt,
                showindex=settings.tables.showindex,
                headers="firstrow",
            )
            + "\n\n"
        )
    return markdown.strip()
