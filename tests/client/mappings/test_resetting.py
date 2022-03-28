def test_resetting_removes_created_stubs(connected_client, random_stub) -> None:
    assert connected_client.stubs.create_stub(random_stub).status_code == 201
    assert connected_client.stubs.get_all_stubs().json()["meta"]["total"] == 1
    assert connected_client.stubs.reset_stub_mappings().status_code == 200
    assert connected_client.stubs.get_all_stubs().json()["meta"]["total"] == 0
