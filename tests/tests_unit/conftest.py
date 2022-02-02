import pytest
from cognite.client.testing import monkeypatch_cognite_client


@pytest.fixture(scope="module")
def mock_cognite_client():
    with monkeypatch_cognite_client() as client_mock:
        yield client_mock
