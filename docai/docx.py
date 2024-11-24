from typing import IO

import docx
from tabulate import tabulate

from docai.document import Document, MetaData
from docai.settings import Settings


def convert_docx(file: IO[bytes], filename: str, settings: Settings | None = None) -> list[Document]:
    """
    Convert docx into documents.

    Parameters
    ----------
    file : IO[bytes]
        _description_
    filename : str
        docx filename
    settings : Settings, optional
        conversion settings, by default Settings()

    Returns
    -------
    list[Document]
        _description_
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
            # TODO: Handle different styles, lists, headings etc
            documents.append(
                Document(
                    content=content.text,
                    metadata=MetaData(filename=filename),
                )
            )
    return documents
