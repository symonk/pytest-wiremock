def test_creating_simple_stub_is_successful(connected_client, random_stub) -> None:
    response = connected_client.stubs.create_stub(random_stub)
    assert response.status_code == 201
    assert connected_client.stubs.delete_stub_with_mapping_id(random_stub.id_).status_code == 200


def test_priority_works_successfully(
    connected_client, mapping_factory, request_factory, response_factory, httpx_session
) -> None:
    one = mapping_factory(request_factory("GET", "/foo"), response_factory(body="first", status=202), priority=2)
    two = mapping_factory(
        request_factory(
            "GET",
            "/foo",
        ),
        response_factory(body="second", status=203),
        priority=1,
    )
    responses = connected_client.stubs.create_stubs((one, two))
    assert all(r.status_code == 201 for r in responses)
    assert httpx_session.get("/foo").status_code == 203
