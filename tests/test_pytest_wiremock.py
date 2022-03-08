from pytest_wiremock import LogNormalSettingsModel
from pytest_wiremock import WiremockClient

pytest_plugins = "pytester"


def test_reset_works_successfully():
    with WiremockClient() as client:
        assert client.reset().status_code == 200
        assert client.update_settings(LogNormalSettingsModel(1, 2, 500)).status_code == 200
