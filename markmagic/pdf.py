"""Convert pdf to markdown."""

from typing import IO

from pypdf import PdfReader

from markmagic.settings import Settings


def convert_pdf(file: str | IO[bytes], settings: Settings) -> str:
    """Convert pdf to markdown."""
    reader = PdfReader(file)
    markdown = ""
    for page in reader.pages:
        markdown += page.extract_text(extraction_mode=settings.pdf.extraction_mode).strip() + "\n\n"
    return markdown.strip()
