"""Detect file type and convert."""

from io import BytesIO

import puremagic

from docai import convert_docx, convert_excel, convert_pdf


def convert_auto(filename: str, content: bytes) -> tuple[str, str]:
    """Convert any file."""
    ext = puremagic.ext_from_filename(filename)  # type: ignore
    _content = BytesIO(content)
    match ext:
        case ".xlsx":
            return ".xlsx", convert_excel(_content)
        case ".docx":
            return ".docx", convert_docx(_content)
        case ".pdf":
            return ".pdf", convert_pdf(_content)
        case _:
            return "unknown", ""
