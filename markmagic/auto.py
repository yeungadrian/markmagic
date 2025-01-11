"""Detect file type and convert."""

from io import BytesIO

import puremagic

from markmagic import convert_docx, convert_eml, convert_excel, convert_pdf
from markmagic.settings import Settings


def convert_auto(filename: str, content: bytes, settings: Settings | None = None) -> tuple[str, str]:
    """Convert any file."""
    if settings is None:
        settings = Settings()
    ext = puremagic.ext_from_filename(filename)
    _content = BytesIO(content)
    markdown = ""
    match ext:
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
                _, _markdown = convert_auto(attachment.filename, attachment.content, settings)
                markdown += _markdown
        case _:
            ext = "unknown"
            markdown = ""
    return ext, markdown
