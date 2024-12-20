"""Convert pdf to markdown."""

from typing import IO

from pypdf import PdfReader

from docai.settings import Settings


def convert_pdf(file: str | IO[bytes], settings: Settings | None = None):
    """Convert pdf to markdown."""
    reader = PdfReader(file)
    markdown = ""
    for page in reader.pages:
        markdown += page.extract_text().strip() + "\n\n"
    return markdown.strip()
