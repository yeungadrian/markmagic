"""Detect file type and convert."""

from io import BytesIO
from pathlib import Path
from typing import Literal

from markmagic.docx import convert_docx
from markmagic.eml import convert_eml
from markmagic.excel import convert_excel
from markmagic.pdf import convert_pdf
from markmagic.settings import Settings


def convert_any(
    filename: str,
    content: bytes,
    ext: Literal[".xlsx", ".docx", ".pdf", ".eml", ""] = "",
    settings: Settings | None = None,
) -> tuple[str | None, str]:
    """Convert any file."""
    if settings is None:
        settings = Settings()
    if ext == "":
        guess = Path(filename).suffix.lower()
    else:
        guess = ext
    _content = BytesIO(content)
    markdown = ""
    match guess:
        case ".xlsx":
            markdown = convert_excel(_content, settings)
        case ".docx":
            markdown = convert_docx(_content, settings)
        case ".pdf":
            markdown = convert_pdf(_content, settings)
        case ".eml":
            _markdown, attachments = convert_eml(_content, settings)
            markdown += _markdown
            for attachment in attachments:
                markdown += f"\n\n## Filename: {attachment.filename}\n\n"
                _, _markdown = convert_any(attachment.filename, attachment.content, "", settings)
                markdown += _markdown
        case _:
            guess = ""
            markdown = ""
    return guess, markdown
