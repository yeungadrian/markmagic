from io import BytesIO

from docai.excel import parse_excel


def test_parse_excel(msft_fs_xlsx: tuple[BytesIO, str]) -> None:
    documents = parse_excel(msft_fs_xlsx[0], msft_fs_xlsx[1])
    assert len(documents) == 12
