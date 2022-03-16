def test_global_fixed_delay(wiremock):
    with wiremock() as client:
        assert client.settings.set_fixed_delay(750).status_code == 200
        response = client.settings.get_settings()
        assert response.status_code == 200
        assert response.json() == {"settings": {"fixedDelay": 750}}
