"""Convert docx files to markdown."""

import re
from typing import IO

import docx
from docx.table import Table
from tabulate import tabulate

from docai.settings import Settings


def _style_text(text: str, style: str, separator: str) -> str:
    # TODO: Review formatting rules
    match style:
        case (
            "List"
            | "List 2"
            | "List 3"
            | "List Bullet"
            | "List Bullet 2"
            | "List Bullet 3"
            | "List Continue"
            | "List Continue 2"
            | "List Continue 3"
            | "List Number"
            | "List Number 2"
            | "List Number 3"
            | "List Paragraph"
        ):
            separator = "\n" + "- "
        case "Heading 1" | "Title":
            separator = "\n\n" + "# "
        case "Subheading" | "Heading 2":
            separator = "\n\n" + "## "
        case "Heading 3":
            separator = "\n\n" + "### "
        case "Heading 4":
            separator = "\n\n" + "#### "
        case "Heading 5" | "Heading 6" | "Heading 7" | "Heading 8" | "Heading 9":
            separator = "\n\n" + "##### "
        case _:
            pass
    text = separator + text
    return text


def convert_docx(file: IO[bytes], settings: Settings | None = None) -> str:
    """Convert docx into documents."""
    if settings is None:
        settings = Settings()
    separator = "\n\n"
    markdown = ""
    document = docx.Document(file)
    for content in document.iter_inner_content():
        if isinstance(content, Table):
            # Normalise whitespace characters to not break github tables
            tabular_data = [[re.sub(r"\s+", " ", cell.text).strip() for cell in row.cells] for row in content.rows]
            markdown += separator + tabulate(
                tabular_data, tablefmt=settings.tables.tablefmt, showindex=settings.tables.showindex, headers="firstrow"
            )
        else:  # Inner contents can only be a Table or Paragraph
            style = content.style.name if content.style is not None else None
            if style is not None:
                markdown += _style_text(content.text.strip(), style, separator)
            else:
                markdown += separator + content.text.strip()
    return markdown
