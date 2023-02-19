import pytest

from sksk_app import create_app, db
from sksk_app.models import User, Level
from sksk_app.utils.auth import UserManager
import sksk_app.utils.edit as editor

@pytest.fixture()
def app():
    app = create_app({
        'TESTING': True
    })
    
    with app.app_context():
        db.create_all()
        level = 'ハン検5級'
        description = '입니다, 고 십다'
        position = 1
        editor.LevelManager.add_level(level, description, position)

        level = 1
        e_group = '指示詞、存在詞、数詞'
        description = '입니다, 있다, 하나'
        position = 1
        editor.E_GroupManager.add_e_group(level, e_group, description, position)
        
        e_group = 1
        element_name = '指示詞'
        description = '입니다'
        position = 1
        editor.ElementManager.add_element(e_group, element_name, description, position)

        element = 1
        japanese = '父は医者です。'
        foreign_l = '아버지는 의사입니다.'
        style = 1
        position = None
        user = 1
        editor.QuestionManager.add_question(element, japanese, foreign_l, style, position, user)

        j_word = '医者'
        f_word = '의사'
        editor.WordManager.add_word(j_word, f_word)

        question = 1
        word = 1
        editor.HintManager.add_hint(question, word)

        name = 'test'
        email = 'test@test.com'
        password = '1234'
        UserManager.register_user(name, email, password)
        UserManager.add_privilege(1, 1)
        UserManager.add_privilege(1, 2)
        UserManager.add_privilege(1, 3)
        UserManager.add_privilege(1, 4)
        
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


