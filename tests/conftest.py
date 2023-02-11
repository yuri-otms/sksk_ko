import pytest
from sksk_app import create_app, db
from sksk_app.models.questions import User, Level
from sksk_app.utils.auth import ManageUser

@pytest.fixture()
def app():
    # database_uri = 'sqlite://'
    database_uri = 'mysql+mysqlconnector://{user}:{password}@{host}:23306/{db_name}?charset=utf8'.format(**{
    'user': 'sksk_ko_test',
    'password': 'teks3A2v',
    'host': '127.0.0.1',
    'db_name': 'sksk_ko_test'
    })
    app = create_app(database_uri)
    app.config['TESTING'] = True

    with app.app_context():
        db.create_all()
        level = db.session.query(Level).first()
        if not level:
            level = 'ハン検5級'
            description = '입니다, 암다'
            position = 1
            new_level = Level(
                level = level,
                description = description,
                position = position
            )
            
            db.session.add(new_level)
            db.session.commit()
        test_user = db.session.query(User).filter(User.email=='test@test.com').first()
        if not test_user:
            name = 'test'
            email = 'test@test.com'
            password = '1234'
            ManageUser.register_user(name, email, password)




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