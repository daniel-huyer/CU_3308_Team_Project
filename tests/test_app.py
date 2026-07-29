def test_app_is_testing(app):
    assert app.config["TESTING"] is True


def test_client_exists(client):
    assert client is not None