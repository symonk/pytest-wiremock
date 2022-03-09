import httpx
import pytest

pytest_plugins = "pytester"


@pytest.fixture(scope="session", autouse=True)
def wiremock_container(docker_ip, docker_services):
    """Create a fresh wiremock container for each test, its lightweight enough"""
    port = docker_services.port_for("wiremock", 8080)
    url = f"http://{docker_ip}:{port}/__admin/"

    def _predicate():
        try:
            return httpx.get(url).status_code == 200
        except Exception:
            return False

    docker_services.wait_until_responsive(check=_predicate, timeout=30.0, pause=1.0)
