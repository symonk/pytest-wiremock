import uuid

import pytest

from pytest_wiremock import ValidationException
from pytest_wiremock.client._exceptions import WiremockNotFoundException


def test_delete_stub_by_uuid_is_successful(connected_client, random_stub) -> None:
    assert connected_client.stubs.create_stub(random_stub).status_code == 201
    assert connected_client.stubs.get_all_stubs().json()["meta"]["total"] == 1
    assert connected_client.stubs.delete_stub_with_mapping_id(random_stub.id_).status_code == 200
    assert connected_client.stubs.get_all_stubs().json()["meta"]["total"] == 0


def test_invalid_uuid_delete_raises(connected_client, random_stub) -> None:
    bad_stub_id = "badly_formatted_uuid"
    assert connected_client.stubs.create_stub(random_stub).status_code == 201
    with pytest.raises(ValidationException) as exc:
        connected_client.stubs.delete_stub_with_mapping_id(bad_stub_id)
    assert exc.value.args[0] == f"uuid={bad_stub_id} is not a valid uuid."


def test_non_existent_compliant_uuid_returns_404(connected_client) -> None:
    with pytest.raises(WiremockNotFoundException):
        assert connected_client.stubs.delete_stub_with_mapping_id(str(uuid.uuid4())).status_code == 404


def test_deleting_all_stubs_works_successfully(connected_client, multi_random_stubs) -> None:
    for stub in multi_random_stubs:
        assert connected_client.stubs.create_stub(stub).status_code == 201
    assert connected_client.stubs.get_all_stubs().json()["meta"]["total"] == 2
    assert connected_client.stubs.delete_all_stubs().status_code == 200
    assert connected_client.stubs.get_all_stubs().json()["meta"]["total"] == 0
