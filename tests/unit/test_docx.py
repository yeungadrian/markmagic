from io import BytesIO

from docai.docx import convert_docx


def test_convert_docx(msft_pr_docx: tuple[BytesIO, str]) -> None:
    """
    Test parse docx function.

    Parameters
    ----------
    msft_pr_docx : tuple[BytesIO, str]
        _description_
    """
    documents = convert_docx(msft_pr_docx[0])
    assert isinstance(documents, str)
