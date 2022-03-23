import uuid

import pytest

from pytest_wiremock.client.resources import Stub
from pytest_wiremock.client.resources import StubRequest
from pytest_wiremock.client.resources import StubResponse


@pytest.fixture
def random_request() -> ...:
    return StubRequest(method="GET", url="/foo/bar")


@pytest.fixture
def random_response() -> ...:
    return StubResponse(status=206, body="Foobar!", status_message="My custom status message!")


@pytest.fixture
def random_stub(random_request, random_response) -> Stub:
    stub = Stub(
        id_=str(uuid.uuid4()),
        name="FooStub",
        request=random_request,
        response=random_response,
    )
    return stub


def test_creating_simple_stub_is_successful(wiremock, random_stub) -> None:
    with wiremock() as client:
        response = client.stubs.create_stub(random_stub)
        assert response.status_code == 201
        assert client.stubs.delete_stub_with_mapping_id(random_stub.id_).status_code == 200