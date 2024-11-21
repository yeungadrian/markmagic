from io import BytesIO
from pathlib import Path

import pytest


@pytest.fixture
def msft_fs_xlsx() -> tuple[str, BytesIO]:
    filename = "tests/data/msft_fs_2024.xlsx"
    return filename, BytesIO(Path(filename).read_bytes())
