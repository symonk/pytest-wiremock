import pytest

from pytest_wiremock import WiremockServerException


def test_delete_stub_by_uuid_is_successful(connected_client, random_stub) -> None:
    assert connected_client.stubs.create_stub(random_stub).status_code == 201
    assert connected_client.stubs.get_all_stubs().json()["meta"]["total"] == 1
    assert connected_client.stubs.delete_stub_with_mapping_id(random_stub.id_).status_code == 200
    assert connected_client.stubs.get_all_stubs().json()["meta"]["total"] == 0


def test_uuid_mismatch_raises_appropriately(connected_client, random_stub) -> None:
    assert connected_client.stubs.create_stub(random_stub).status_code == 201
    with pytest.raises(WiremockServerException) as exc:
        connected_client.stubs.delete_stub_with_mapping_id("unknown")
    assert exc.value.args[0] == b"Server Error"
    assert exc.value.status_code == 500


def test_deleting_all_stubs_works_successfully(connected_client, multi_random_stubs) -> None:
    for stub in multi_random_stubs:
        assert connected_client.stubs.create_stub(stub).status_code == 201
    assert connected_client.stubs.get_all_stubs().json()['meta']['total'] == 2
    assert connected_client.stubs.delete_all_stubs().status_code == 200
    assert connected_client.stubs.get_all_stubs().json()['meta']['total'] == 0
