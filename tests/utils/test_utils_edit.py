from sksk_app import db
from sksk_app.models import Level, E_Group, Element, Question
import sksk_app.utils.edit as editor

# LevelManager
def test_add_level(app):
    level_name = "ハン検4級"
    description = "거예요, 아서, 러"
    position = 3
    with app.app_context():
        editor.LevelManager.add_level(level_name,description, position)
        level = Level.query.filter(Level.level==level_name)
    
    assert level is not None

# E_GroupManager
def test_add_e_group(app):
    level = 1
    e_group_name = "グループ1"
    description = "입나다, 고 십다"
    position = None
    with app.app_context():
        editor.E_GroupManager.add_e_group(level, e_group_name, description, position)
        e_group = E_Group.query.filter(E_Group.e_group==e_group_name)

    assert e_group is not None

# ElementManager
def test_add_element(app):
    e_group = 1
    element_name = '指示詞'
    description = '입니다'
    position = None
    with app.app_context():
        editor.ElementManager.add_element(e_group, element_name, description, position)
        element = Element.query.filter(Element.element==element_name)

    assert element is not None

# QuestionManager
def test_add_question(app):
    element = 1
    japanese = '父は医者です。'
    foreign_l = '저는 학생입니다.'
    style = 1
    position = None
    user = 1
    with app.app_context():
        editor.QuestionManager.add_question(element, japanese, foreign_l, style, position, user)
        question = Question.query.filter(Question.japanese==japanese)

    assert question is not None