from pytest_wiremock import WiremockClient

pytest_plugins = "pytester"


def test_reset_works_successfully():
    with WiremockClient() as client:
        assert client.reset().status_code == 200
        assert client.set_global_fixed_delay(1000)
