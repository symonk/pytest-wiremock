import pytest

from pytest_wiremock import WiremockFacade


@pytest.fixture(scope="session")
def wiremock(request):
    return WiremockFacade
