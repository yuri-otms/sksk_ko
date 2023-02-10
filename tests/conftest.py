import pytest
from sksk_app import create_app, db

@pytest.fixture()
def app():
    app = create_app()

    with app.app_context():
        db.create_all()

    yield app

@pytest.fixture()
def client(app):
    return app.test_client()

class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, email='test@test.com', password='1234'):
        return self._client.post(
            '/auth/login',
            data={'email': email, 'password': password}
        )

    def logout(self):
        return self._client.get('/auth/logout')

@pytest.fixture
def auth(client):
    return AuthActions(client)