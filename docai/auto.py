"""Detect file type and convert."""

from io import BytesIO

import puremagic

from docai import convert_docx, convert_eml, convert_excel, convert_pdf


def convert_auto(filename: str, content: bytes) -> tuple[str, str]:
    """Convert any file."""
    ext = puremagic.ext_from_filename(filename)  # type: ignore
    _content = BytesIO(content)
    markdown = ""
    match ext:
        case ".xlsx":
            markdown = convert_excel(_content)
        case ".docx":
            markdown = convert_docx(_content)
        case ".pdf":
            markdown = convert_pdf(_content)
        case ".eml":
            _markdown, attachments = convert_eml(_content)
            markdown += _markdown
            for attachment in attachments:
                markdown += f"\n\n## Filename: {attachment.filename}\n\n"
                _, _markdown = convert_auto(attachment.filename, attachment.content)
                markdown += _markdown
        case _:
            ext = "unknown"
            markdown = ""
    return ext, markdown
