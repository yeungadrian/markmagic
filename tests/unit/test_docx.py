from io import BytesIO

from docai.docx import partition_docx


def test_partition_docx(msft_pr_docx: tuple[BytesIO, str]) -> None:
    """
    Test partition docx function.

    Parameters
    ----------
    msft_pr_docx : tuple[BytesIO, str]
        _description_
    """
    documents = partition_docx(*msft_pr_docx)
    assert len(documents.chunks) == 166 # Check number of sections
