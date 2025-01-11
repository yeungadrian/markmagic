from io import BytesIO
from pathlib import Path

from markmagic.docx import convert_docx


def test_convert_docx() -> None:
    """Test convert docx function."""
    filename = "tests/data/docx/msft_pr.docx"
    markdown = convert_docx(BytesIO(Path(filename).read_bytes()))
    with Path("tests/data/docx/msft_pr.md").open() as f:
        expected_results = f.read()
    assert markdown == expected_results
