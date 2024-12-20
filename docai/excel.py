"""Convert excel files to markdown."""

from typing import IO

from python_calamine import CalamineWorkbook
from tabulate import tabulate

from docai.settings import Settings


def convert_excel(file: IO[bytes], settings: Settings | None = None) -> list[str]:
    """Partition an excel workbook."""
    if settings is None:
        settings = Settings()
    workbook = CalamineWorkbook.from_object(file)  # type: ignore
    markdowns: list[str] = []
    for sheet_name in workbook.sheet_names:
        calamine_sheet = workbook.get_sheet_by_name(sheet_name)
        tabular_data = calamine_sheet.to_python(skip_empty_area=settings.excel.skip_empty_area)
        markdowns.append(
            tabulate(
                tabular_data,
                tablefmt=settings.tables.tablefmt,
                showindex=settings.tables.showindex,
            )
        )
    return markdowns
