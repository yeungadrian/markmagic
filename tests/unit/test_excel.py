from io import BytesIO
from pathlib import Path

from docai.excel import convert_excel


def test_convert_excel() -> None:
    """Test convert excel function."""
    filename = "tests/data/excel/msft_fs.xlsx"
    markdown = convert_excel(BytesIO(Path(filename).read_bytes()))
    with Path("tests/data/excel/msft_fs.md").open() as f:
        expected_results = f.read()
    assert markdown == expected_results
