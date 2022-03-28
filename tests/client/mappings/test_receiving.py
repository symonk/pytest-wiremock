import pytest


@pytest.mark.skip(reason="Metadata is a work in progress.")
def test_find_by_metadata_works(connected_client, mapping_factory, request_factory, httpx_session) -> None:
    mapping = mapping_factory(request_factory("GET", "/metadata"), metadata={"foo": "bar"})
    connected_client.stubs.create_stub(mapping)
    response = connected_client.stubs.find_by_metadata()  # noqa
