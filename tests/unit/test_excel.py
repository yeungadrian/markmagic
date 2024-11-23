from io import BytesIO

from docai.excel import parse_excel


def test_parse_excel(msft_fs_xlsx: tuple[BytesIO, str]) -> None:
    """
    Test parse excel function.

    Parameters
    ----------
    msft_fs_xlsx : tuple[BytesIO, str]
        _description_
    """
    documents = parse_excel(msft_fs_xlsx[0], msft_fs_xlsx[1])
    assert len(documents) == 12
