from typing import IO

import docx
from tabulate import tabulate

from docai.document import Document, MetaData
from docai.settings import Settings


def convert_docx(file: IO[bytes], filename: str, settings: Settings | None = None) -> list[Document]:
    """
    Convert a DOCX file into a list of Document objects.

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
    list[Document]
        A list of Document objects containing the converted content and metadata.
    """
    if settings is None:
        settings = Settings()
    documents = []
    for content in docx.Document(file).iter_inner_content():
        if isinstance(content, docx.table.Table):
            tabular_data = [[cell.text for cell in row.cells] for row in content.rows]
            documents.append(
                Document(
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
            documents.append(
                Document(
                    content=content.text,
                    metadata=MetaData(filename=filename),
                )
            )
    return documents
