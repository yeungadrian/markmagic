from typing import IO

from python_calamine import CalamineWorkbook
from tabulate import tabulate

from docai.models import Chunk, MetaData, PartitionedDocument
from docai.settings import Settings


def partition_excel(
    file: IO[bytes], filename: str, settings: Settings | None = None
) -> list[PartitionedDocument]:
    """
    Partition each excel sheet into a PartitionedDocument.

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
    Document
        A list of chunks, with metadata of excel file.
    """
    if settings is None:
        settings = Settings()
    workbook = CalamineWorkbook.from_object(file)
    partitions = []
    for sheet_name in workbook.sheet_names:
        calamine_sheet = workbook.get_sheet_by_name(sheet_name)
        tabular_data = calamine_sheet.to_python(skip_empty_area=settings.excel.skip_empty_area)
        partition = PartitionedDocument(
            chunks=[
                Chunk(
                    content=tabulate(
                        tabular_data,
                        tablefmt=settings.tables.tablefmt,
                        showindex=settings.tables.showindex,
                    ),
                    table=True,
                )
            ],
            metadata=MetaData(filename=filename, sheet_name=sheet_name),
        )
        partitions.append(partition)
    return partitions
