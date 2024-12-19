"""Convert docx files to markdown."""

import re
from typing import IO

import docx
from tabulate import tabulate

from docai.settings import Settings


def _style_text(text: str, style: str, separator: str) -> str:
    text = "\n" + "- " + text if "List" in style else separator + text
    return text


def convert_docx(file: IO[bytes], settings: Settings | None = None) -> str:
    """Convert docx into documents."""
    if settings is None:
        settings = Settings()
    markdown = ""
    for n, content in enumerate(docx.Document(file).iter_inner_content()):
        separator = "" if n == 0 else "\n\n"
        if isinstance(content, docx.table.Table):
            tabular_data = [[re.sub(r"\s+", " ", cell.text).strip() for cell in row.cells] for row in content.rows]
            markdown += "\n\n" + tabulate(
                tabular_data,
                tablefmt=settings.tables.tablefmt,
                showindex=settings.tables.showindex,
                headers=settings.tables.headers,
            )
        elif isinstance(content, docx.text.paragraph.Paragraph):
            # TODO: Handle different styles, lists, headings etc
            markdown += _style_text(content.text, content.style.name, separator)
    return markdown
