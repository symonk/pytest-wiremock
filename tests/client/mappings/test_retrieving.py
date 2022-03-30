import pytest

from pytest_wiremock import MatchingJsonPath


@pytest.mark.skip(reason="Work in progress")
def test_find_by_string_equals_meta_data(connected_client, mapping_factory, request_factory, httpx_session) -> None:
    mapping = mapping_factory(request_factory("GET", "/metadata"), metadata={"foo": 1337})
    connected_client.stubs.create_stub(mapping)
    matcher = MatchingJsonPath(expression="$.foo", contains="123")
    response = connected_client.stubs.find_by_metadata(matcher)  # noqa
