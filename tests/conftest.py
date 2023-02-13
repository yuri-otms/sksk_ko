import pytest

from sksk_app import create_app, db
from sksk_app.models import User, Level
from sksk_app.utils.auth import UserManager
from sksk_app.utils.questions import QuestionManager

@pytest.fixture()
def app():
    app = create_app({
        'TESTING': True
    })
    
    with app.app_context():
        db.create_all()
        level = 'ハン検5級'
        description = '입니다, 암다'
        position = 1
        QuestionManager.insert_level(level, description, position)

        name = 'test'
        email = 'test@test.com'
        password = '1234'
        UserManager.register_user(name, email, password)
        UserManager.add_privilege(1, 1)
        
        db.session.begin_nested()

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

@pytest.fixture(scope='function', autouse=True)
def session(app):
    yield 
    with app.app_context():
        db.session.rollback()

# @pytest.fixture(scope='function', autouse=True)
# def scope_function(app):
#     yield 
#     with app.app_context():
#         QuestionManager.delete_testing_levels()


