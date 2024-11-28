from typing import IO

from python_calamine import CalamineWorkbook
from tabulate import tabulate

from docai.document import Document, MetaData
from docai.settings import Settings


def convert_excel(file: IO[bytes], filename: str, settings: Settings | None = None) -> list[Document]:
    """
    Convert excel into list of documents.

    Parameters
    ----------
    file : IO[bytes]
        The excel file as a byte stream.
    filename : str
        The name of the excel file.
    settings : Settings, optional
        Conversion settings, by default None. If not provided, default settings will be used.

    Returns
    -------
    list[Document]
        A list of Document objects containing the converted content and metadata.
    """
    if settings is None:
        settings = Settings()
    workbook = CalamineWorkbook.from_object(file)
    documents = []
    for sheet_name in workbook.sheet_names:
        calamine_sheet = workbook.get_sheet_by_name(sheet_name)
        tabular_data = calamine_sheet.to_python(skip_empty_area=settings.excel.skip_empty_area)
        documents.append(
            Document(
                content=tabulate(
                    tabular_data,
                    tablefmt=settings.tables.tablefmt,
                    showindex=settings.tables.showindex,
                ),
                metadata=MetaData(
                    sheet_name=sheet_name, filename=filename, table=True, raw_table=tabular_data
                ),
            )
        )
    return documents
