"""Convert pdf to markdown."""

import base64
from io import BytesIO
from typing import IO

import pypdfium2 as pdfium
from openai import OpenAI
from pypdf import PdfReader

from markmagic.settings import Settings


def convert_pdf(file: str | IO[bytes], settings: Settings) -> str:
    """Convert pdf to markdown."""
    reader = PdfReader(file)
    markdown = ""
    for page in reader.pages:
        markdown += page.extract_text(extraction_mode=settings.extraction_mode).strip() + "\n\n"
    return markdown.strip()


instructions = """Convert the provided image into Markdown format. Ensure that all content from the page is included, such as headers, footers, subtexts, images (with alt text if possible), tables, and any other elements.

  Requirements:

  - Output Only Markdown: Return solely the Markdown content without any additional explanations or comments.
  - No Delimiters: Do not use code fences or delimiters like ```markdown.
  - Complete Content: Do not omit any part of the page, including headers, footers, tables and subtext."""  # noqa: E501


def _convert_pdf_to_base64(page: pdfium.PdfPage) -> str:
    bitmap = page.render(
        scale=5,  # 360dpi resolution
        rotation=0,  # no additional rotation
    )
    pil_image = bitmap.to_pil()
    buffer = BytesIO()
    pil_image.save(buffer, format="JPEG")
    base64_image = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return base64_image


def _ocr_with_vlm(client: OpenAI, base64_image: str, settings: Settings) -> str:
    response = client.chat.completions.create(
        model=settings.model,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": instructions},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                    },
                ],
            },
        ],
        stop=settings.stop,
        temperature=0.0,
    )
    if response.choices[0].message.content is None:
        return ""
    else:
        return response.choices[0].message.content


def convert_pdf_with_vlm(file: str | IO[bytes], settings: Settings) -> str:
    """Convert pdf to markdown using vision language model."""
    markdown = ""
    pdf = pdfium.PdfDocument(file.read())  # type: ignore
    n_pages = len(pdf)

    if settings.api_key is None:
        api_key = ""
    else:
        api_key = settings.api_key.get_secret_value()

    client = OpenAI(
        api_key=api_key,
        base_url=settings.base_url,
    )

    for i in range(n_pages):
        page = pdf.get_page(i)
        base64_image = _convert_pdf_to_base64(page)
        markdown += _ocr_with_vlm(client, base64_image, settings)
    return markdown
