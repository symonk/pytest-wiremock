def test_creating_simple_stub_is_successful(wiremock, random_stub) -> None:
    with wiremock() as client:
        response = client.stubs.create_stub(random_stub)
        assert response.status_code == 201
        assert client.stubs.delete_stub_with_mapping_id(random_stub.id_).status_code == 200
