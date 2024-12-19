from io import BytesIO
from pathlib import Path

import pytest


@pytest.fixture
def msft_pr_docx() -> tuple[BytesIO, str]:
    """Load MSFT docx as BytesIO."""
    filename = "tests/data/msft_pr_24q4.docx"
    return BytesIO(Path(filename).read_bytes()), filename


