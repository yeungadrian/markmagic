from pathlib import Path

from markmagic import convert_any
from markmagic.settings import EmailSettings, Settings


def test_convert_any_docx() -> None:
    """Test convert any function for docx."""
    filename = "tests/data/docx/msft_pr.docx"
    with Path(filename).open("rb") as f:
        ext, markdown = convert_any(filename, f)
    with Path("tests/data/docx/msft_pr.md").open() as f:
        expected_results = f.read()
    assert ext == ".docx"
    assert markdown == expected_results


def test_convert_any_excel() -> None:
    """Test convert any function for excel."""
    filename = "tests/data/excel/msft_fs.xlsx"
    with Path(filename).open("rb") as f:
        ext, markdown = convert_any(filename, f)
    with Path("tests/data/excel/msft_fs.md").open() as f:
        expected_results = f.read()
    assert ext == ".xlsx"
    assert markdown == expected_results


def test_convert_any_pdf() -> None:
    """Test convert any function for pdf."""
    filename = "tests/data/pdf/msft_ar.pdf"
    with Path(filename).open("rb") as f:
        ext, markdown = convert_any(filename, f)
    with Path("tests/data/pdf/msft_ar.md").open() as f:
        expected_results = f.read()
    assert ext == ".pdf"
    assert markdown == expected_results


def test_convert_any_html_eml() -> None:
    """Test convert any function for email."""
    filename = "tests/data/eml/html_w_att.eml"
    with Path(filename).open("rb") as f:
        ext, markdown = convert_any(filename, f)
    with Path("tests/data/eml/html_w_att.md").open() as f:
        expected_results = f.read()
    assert ext == ".eml"
    assert markdown == expected_results


def test_convert_any_plain_eml() -> None:
    """Test convert any function for email."""
    filename = "tests/data/eml/plain.eml"
    with Path(filename).open("rb") as f:
        ext, markdown = convert_any(filename, f)
    with Path("tests/data/eml/plain.md").open() as f:
        expected_results = f.read()
    assert ext == ".eml"
    assert markdown == expected_results


def test_convert_any_html_eml_skip_attachment() -> None:
    """Test convert any function for email, but skip attachments."""
    settings = Settings(email=EmailSettings(process_attachments=False))
    filename = "tests/data/eml/html_w_att.eml"
    with Path(filename).open("rb") as f:
        ext, markdown = convert_any(filename, f, ".eml", settings=settings)
    with Path("tests/data/eml/html_wo_att.md").open() as f:
        expected_results = f.read()
    assert ext == ".eml"
    assert markdown == expected_results


def test_convert_any_zip() -> None:
    """Test convert any function for zip."""
    filename = "tests/data/unknown/msft_pr.zip"
    with Path(filename).open("rb") as f:
        ext, markdown = convert_any(filename, f)
    assert ext == ""
    assert markdown == ""
