import pytest
from pydantic import ValidationError

from markmagic.settings import Settings, TableSettings


def test_valid_tabulate_format():
    """Test valid tabulate format."""
    valid_settings = Settings(tables=TableSettings(tablefmt="github"))
    assert isinstance(valid_settings, Settings)


def test_invalid_tabulate_format():
    """Test invalid tabulate format."""
    with pytest.raises(ValidationError):
        Settings(tables=TableSettings(tablefmt="invalid"))
