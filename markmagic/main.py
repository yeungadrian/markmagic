"""Detect file type and convert."""

from io import BytesIO
from pathlib import Path
from typing import IO

from markmagic.docx import convert_docx
from markmagic.eml import convert_eml
from markmagic.excel import convert_excel
from markmagic.pdf import convert_pdf, convert_pdf_with_vlm
from markmagic.settings import Settings


def convert_any(
    filename: str,
    file: IO[bytes],
    ext: str = "",
    settings: Settings | None = None,
) -> tuple[str, str]:
    """Automatically convert any file into markdown.

    Parameters
    ----------
    filename : str
    file : IO[bytes]
        file as buffer, e.g.
        - pass f when using with Path(...).open("rb") as f:
        - or create buffer by wrapping bytes in BytesIO

    ext : str, optional
        extension of file, by default "" to automatically detect
    settings : Settings | None, optional
        conversion settings to apply, by default None

    Returns
    -------
    tuple[str, str]
        extension, markdown of file
    """
    if settings is None:
        settings = Settings()
    if ext == "":
        _ext = Path(filename).suffix.lower()
    else:
        _ext = ext
    markdown = ""
    match _ext:
        case ".xlsx":
            markdown = convert_excel(file, settings)
        case ".docx":
            markdown = convert_docx(file, settings)
        case ".pdf":
            if settings.use_vlm:
                markdown = convert_pdf_with_vlm(file, settings)
            else:
                markdown = convert_pdf(file, settings)
        case ".eml":
            _markdown, attachments = convert_eml(file, settings)
            markdown += _markdown
            for attachment in attachments:
                markdown += f"\n\n## Filename: {attachment.filename}\n\n"
                _, _markdown = convert_any(attachment.filename, BytesIO(attachment.content), "", settings)
                markdown += _markdown
        case _:
            _ext = ""
            markdown = ""
    return _ext, markdown
