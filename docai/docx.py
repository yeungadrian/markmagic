from typing import IO

import docx
from tabulate import tabulate

from docai.models import Chunk, MetaData, PartitionedDocument
from docai.settings import Settings


def partition_docx(file: IO[bytes], filename: str, settings: Settings | None = None) -> PartitionedDocument:
    """
    Partition a DOCX file into a PartitionedDocument.

    Parameters
    ----------
    file : IO[bytes]
        The DOCX file as a byte stream.
    filename : str
        The name of the DOCX file.
    settings : Settings, optional
        Conversion settings, by default None. If not provided, default settings will be used.

    Returns
    -------
    PartitionedDocument
        A list of chunks for each paragraph or table, with metadata for DOCX file.
    """
    if settings is None:
        settings = Settings()
    chunks = []
    for content in docx.Document(file).iter_inner_content():
        if isinstance(content, docx.table.Table):
            tabular_data = [[cell.text for cell in row.cells] for row in content.rows]
            chunks.append(
                Chunk(
                    content=tabulate(
                        tabular_data,
                        tablefmt=settings.tables.tablefmt,
                        showindex=settings.tables.showindex,
                    ),
                    table=True,
                ),
            )
        elif isinstance(content, docx.text.paragraph.Paragraph):
            # TODO: Format different styles, lists, headings etc
            chunks.append(
                Chunk(
                    content=content.text,
                )
            )
    return PartitionedDocument(chunks=chunks, metadata=MetaData(filename=filename))
