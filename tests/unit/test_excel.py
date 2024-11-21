from io import BytesIO

from docai.excel import parse_excel


def test_parse_excel(msft_fs_xlsx: tuple[str, BytesIO]) -> None:
    documents = parse_excel(msft_fs_xlsx[1], msft_fs_xlsx[0])
    assert len(documents) == 12
