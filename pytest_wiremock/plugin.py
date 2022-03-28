import pytest

from pytest_wiremock import WiremockClient


@pytest.fixture(scope="session")
def wiremock():
    return WiremockClient
