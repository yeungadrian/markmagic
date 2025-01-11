from io import BytesIO
from pathlib import Path

from markmagic.pdf import convert_pdf


def test_convert_pdf() -> None:
    """Test convert pdf function."""
    filename = "tests/data/pdf/msft_ar.pdf"
    markdown = convert_pdf(BytesIO(Path(filename).read_bytes()))
    with Path("tests/data/pdf/msft_ar.md").open() as f:
        expected_results = f.read()
    assert markdown == expected_results
