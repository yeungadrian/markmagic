from io import BytesIO
from pathlib import Path

import pytest


@pytest.fixture
def msft_fs_xlsx() -> tuple[BytesIO, str]:
    filename = "tests/data/msft_fs_24.xlsx"
    return BytesIO(Path(filename).read_bytes()), filename


@pytest.fixture
def msft_pr_docx() -> tuple[BytesIO, str]:
    filename = "tests/data/msft_pr_24q4.docx"
    return BytesIO(Path(filename).read_bytes()), filename
