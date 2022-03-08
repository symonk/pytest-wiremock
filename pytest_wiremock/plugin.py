import pytest

from pytest_wiremock import WiremockClient


@pytest.fixture(scope="session")
def pytest_wiremock(request):
    return WiremockClient
