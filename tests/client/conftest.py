import typing
import uuid

import pytest

from pytest_wiremock import WiremockClient
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


@pytest.fixture
def multi_random_stubs(random_request, random_response) -> typing.List[Stub]:
    return [
        Stub(id_=str(uuid.uuid4()), name=f"Random{n}", request=random_request, response=random_response)
        for n in range(2)
    ]


@pytest.fixture
def connected_client(wiremock_container) -> WiremockClient:
    """A Simple API client; connected to the running test wiremock instance."""
    with WiremockClient() as client:
        yield client
