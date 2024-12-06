from typing import IO

import docx
from tabulate import tabulate

from docai.models import Chunk, Document, MetaData
from docai.settings import Settings


def convert_docx(file: IO[bytes], filename: str, settings: Settings | None = None) -> Document:
    """
    Convert a DOCX file into a list of chunk objects.

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
    list[Chunk]
        A list of Chunk objects containing the converted content and metadata.
    """
    if settings is None:
        settings = Settings()
    chunks = []
    for content in docx.Chunk(file).iter_inner_content():
        if isinstance(content, docx.table.Table):
            tabular_data = [[cell.text for cell in row.cells] for row in content.rows]
            chunks.append(
                Chunk(
                    content=tabulate(
                        tabular_data,
                        tablefmt=settings.tables.tablefmt,
                        showindex=settings.tables.showindex,
                    ),
                    metadata=MetaData(filename=filename, table=True, raw_table=tabular_data),
                )
            )
        elif isinstance(content, docx.text.paragraph.Paragraph):
            # TODO: Format different styles, lists, headings etc
            chunks.append(
                Chunk(
                    content=content.text,
                    metadata=MetaData(filename=filename),
                )
            )
    return Document(chunks=chunks)
