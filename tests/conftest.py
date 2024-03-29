import pytest

from sksk_app import create_app, db
from sksk_app.models import User, Grade
import sksk_app.utils.user as user_setting
import sksk_app.utils.edit as editor

@pytest.fixture()
def app():
    app = create_app({
        'TESTING': True
    })
    
    with app.app_context():
        db.create_all()
        grade = 'ハン検5級'
        description = '입니다, 고 십다'
        editor.GradeManager.add_grade(grade, description)

        grade = 1
        e_group = '指示詞、存在詞、数詞'
        description = '입니다, 있다, 하나'
        editor.E_GroupManager.add_e_group(grade, e_group, description)
        
        e_group = 1
        element_name = '指示詞'
        description = '입니다'
        position = 1
        editor.ElementManager.add_element(e_group, element_name, description)

        element = 1
        level = 1
        japanese = '父は医者です。'
        foreign_l = '아버지는 의사입니다.'
        style = 1
        spoken = 0
        sida = 0
        will = 0
        user = 1
        editor.QuestionManager.add_question(element, level, japanese, foreign_l, style, spoken, sida, will, user)

        element = 1
        level = 1
        japanese = '私は学生です。'
        foreign_l = '저는 학생입니다.'
        style = 1
        user = 1
        editor.QuestionManager.add_question(element, level, japanese, foreign_l, style, spoken, sida, will, user)


        element = 1
        level = 1
        japanese = '母は公務員です。'
        foreign_l = '어머니는 공무원입니다.'
        style = 1
        position = None
        user = 1
        editor.QuestionManager.add_question(element, level, japanese, foreign_l, style, spoken, sida, will, user)


        japanese_word = '医者'
        foreign_word = '의사'
        editor.WordManager.add_word(japanese_word, foreign_word)

        question = 1
        word = 1
        editor.HintManager.add_hint(question, word)


        style = 'ハムニダ体'
        editor.StyleManager.add_style(style)
        style = 'ヘヨ体'
        editor.StyleManager.add_style(style)
        style = 'ヘ体'
        editor.StyleManager.add_style(style)
        style = 'ハンダ体'
        editor.StyleManager.add_style(style)
        style = 'ハオ体'
        editor.StyleManager.add_style(style)

        name = 'test'
        email = 'test@test.com'
        password = '1234'
        user_setting.UserManager.register_user(name, email, password)
        user_setting.UserManager.add_privilege(1, 1)
        user_setting.UserManager.add_privilege(1, 2)
        user_setting.UserManager.add_privilege(1, 3)
        user_setting.UserManager.add_privilege(1, 4)
        
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
            data={'email': email, 'password': password, 'question':0}
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
#         QuestionManager.delete_testing_grades()


