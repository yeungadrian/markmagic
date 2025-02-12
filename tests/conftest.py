import pytest


@pytest.fixture(scope="session")
def vcr_config():
    return {
        "filter_headers": ["authorization"],
        "ignore_localhost": True,
        # Instruct VCR that we want to record the interaction only once.
        "record_mode": "once",
    }
