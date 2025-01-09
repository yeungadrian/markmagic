"""Convert eml to markdown."""

import email
import email.policy
from email.message import EmailMessage
from typing import IO, cast

from markdownify import markdownify as md

from docai.settings import Settings


def _extract_body(message: EmailMessage) -> str:
    body = message.get_body()
    if body is None:
        body_content = ""
    else:
        body_content = ""
        content_type = body.get_content_type()
        if content_type == "text/html":
            body_content = md(body.get_content())
        elif content_type == "text/plain":
            body_content = body.get_content()
    return body_content


def convert_eml(file: str | IO[bytes], settings: Settings | None = None) -> str:
    """Convert eml to markdown."""
    if settings is None:
        settings = Settings()
    message = cast(EmailMessage, email.message_from_binary_file(file, policy=email.policy.default))  # type: ignore
    body_content = _extract_body(message)
    return body_content
