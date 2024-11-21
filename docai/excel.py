from typing import IO

from python_calamine import CalamineWorkbook
from tabulate import tabulate

from docai.document import Document, MetaData


def parse_excel(file: IO[bytes], filename: str) -> list[Document]:
    workbook = CalamineWorkbook.from_object(file)
    documents = []
    for sheet_name in workbook.sheet_names:
        sheet = workbook.get_sheet_by_name(sheet_name)
        table = sheet.to_python(skip_empty_area=False)
        documents.append(
            Document(
                content=tabulate(table, tablefmt="github", showindex="always"),
                metadata=MetaData(sheet_name=sheet_name, filename=filename),
            )
        )

    return documents
