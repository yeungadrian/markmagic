from io import BytesIO

from docai.excel import partition_excel


def test_partition_excel(msft_fs_xlsx: tuple[BytesIO, str]) -> None:
    """
    Test partition excel function.

    Parameters
    ----------
    msft_fs_xlsx : tuple[BytesIO, str]
        _description_
    """
    documents = partition_excel(*msft_fs_xlsx)
    assert len(documents) == 12  # Check number of sheets
