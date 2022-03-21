import uuid

import pytest

from pytest_wiremock.client.resources import Stub
from pytest_wiremock.client.resources import StubRequest
from pytest_wiremock.client.resources import StubResponse


@pytest.fixture
def random_request() -> ...:
    return StubRequest()


@pytest.fixture
def random_response() -> ...:
    return StubResponse()


@pytest.fixture
def random_stub(random_request, random_response) -> Stub:
    stub = Stub(
        id_=100,
        uuid=str(uuid.uuid4()),
        name="foo",
        request=random_request,
        response=random_response,
        persistent=False,
        priority=1,
        scenario_name="scenario name",
        required_scenario_state="nostate",
        new_scenario_state="newstate",
        post_serve_actions={},
        metadata={},
    )
    return stub


def test_creating_simple_stub_is_successful(wiremock, random_stub) -> None:
    with wiremock() as client:
        client.stubs.create_new_stub()
