"""Convert eml to markdown."""

import email
import email.policy
from email.message import EmailMessage
from typing import IO, cast

from markdownify import markdownify
from pydantic import BaseModel

from markmagic.settings import Settings


class Attachment(BaseModel):
    """Attachment."""

    filename: str
    content: bytes


def _extract_body(message: EmailMessage) -> str:
    """Extract main email body."""
    body = message.get_body()
    if body is None:
        body_content = ""
    else:
        body_content = ""
        content_type = body.get_content_type()
        if content_type == "text/html":
            body_content = markdownify(body.get_content())
        elif content_type == "text/plain":
            body_content = body.get_content()
    return body_content.strip()


def _extract_attachments(message: EmailMessage):
    """Extract all valid attachments."""
    attachments: list[Attachment] = []
    for i in message.iter_attachments():
        filename = i.get_filename()
        if filename is not None:
            content = i.get_content()
            if isinstance(content, str):
                content = content.encode("utf-8")
            elif isinstance(content, bytes):
                pass
            else:
                continue
            attachments.append(Attachment(filename=filename, content=content))
    return attachments


def convert_eml(file: str | IO[bytes], settings: Settings) -> tuple[str, list[Attachment]]:
    """Convert eml to markdown."""
    message = cast(EmailMessage, email.message_from_binary_file(file, policy=email.policy.default))  # type: ignore
    # TODO: Add subject, to, from
    body_content = _extract_body(message)
    if settings.email.process_attachments:
        attachments = _extract_attachments(message)
    else:
        attachments = []
    return body_content, attachments
