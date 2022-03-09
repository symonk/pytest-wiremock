def test_reset_works_successfully(wiremock):
    with wiremock() as client:
        assert client.reset().status_code == 200
