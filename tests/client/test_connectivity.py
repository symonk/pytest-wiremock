import pytest

from pytest_wiremock.client._exceptions import WiremockConnectionError


def test_connection_failed(wiremock) -> None:
    with pytest.raises(WiremockConnectionError) as error:
        with wiremock(port=9999) as client:
            client.reset()
    assert error.value.args[0] == "Unable to connect to a wiremock instance running on: http://localhost:9999/__admin/"


def test_connection_success(wiremock) -> None:
    with wiremock() as client:
        assert client.reset().status_code == 200
