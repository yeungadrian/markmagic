from io import BytesIO

from docai.docx import parse_docx


def test_parse_excel(msft_pr_docx: tuple[BytesIO, str]) -> None:
    documents = parse_docx(msft_pr_docx[0], msft_pr_docx[1])
    assert len(documents) == 166
