from pytest_wiremock import WiremockClient

pytest_plugins = "pytester"


def test_reset_works_successfully():
    with WiremockClient("localhost", 8080) as client:
        assert client.reset().status_code == 200
