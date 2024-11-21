from typing import IO

from python_calamine import CalamineWorkbook
from tabulate import tabulate

from docai.document import Document, MetaData
from docai.settings import Settings


def parse_excel(
    file: IO[bytes], filename: str, settings: Settings = Settings()
) -> list[Document]:
    workbook = CalamineWorkbook.from_object(file)
    documents = []
    for sheet_name in workbook.sheet_names:
        calamine_sheet = workbook.get_sheet_by_name(sheet_name)
        tabular_data = calamine_sheet.to_python(skip_empty_area=False)
        documents.append(
            Document(
                content=tabulate(
                    tabular_data,
                    tablefmt=settings.tables.tablefmt,
                    showindex=settings.tables.showindex,
                ),
                metadata=MetaData(sheet_name=sheet_name, filename=filename),
            )
        )

    return documents
