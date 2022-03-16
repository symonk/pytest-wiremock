import pytest

pytest_plugins = "pytester"


@pytest.fixture(scope="session", autouse=True)
def wiremock_container(docker_services):
    """Create a fresh wiremock container for each test, its lightweight enough"""
    docker_services.start("wiremock")
    docker_services.wait_for_service("wiremock", 8080)
