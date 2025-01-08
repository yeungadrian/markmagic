from pathlib import Path

from docai.auto import convert_auto


def test_convert_auto_docx() -> None:
    """Test convert auto function for docs."""
    filename = "tests/data/docx/msft_pr.docx"
    ext, markdown = convert_auto(filename, Path(filename).read_bytes())
    with Path("tests/data/docx/msft_pr.md").open() as f:
        expected_results = f.read()
    assert markdown == expected_results


def test_convert_auto_excel() -> None:
    """Test convert auto function for excel."""
    filename = "tests/data/excel/msft_fs.xlsx"
    ext, markdown = convert_auto(filename, Path(filename).read_bytes())
    with Path("tests/data/excel/msft_fs.md").open() as f:
        expected_results = f.read()
    assert markdown == expected_results


def test_convert_auto_pdf() -> None:
    """Test convert auto function for pdf."""
    filename = "tests/data/pdf/msft_ar.pdf"
    ext, markdown = convert_auto(filename, Path(filename).read_bytes())
    with Path("tests/data/pdf/msft_ar.md").open() as f:
        expected_results = f.read()
    assert markdown == expected_results
