from sksk_app import db
from sksk_app.models import Level, E_Group, Element, Question, Word, Hint
import sksk_app.utils.edit as editor

# LevelManager
def test_add_level(app):
    level_name = 'ハン検4級'
    description = '거예요, 아서, 러'
    position = 3
    with app.app_context():
        editor.LevelManager.add_level(level_name,description, position)
        level = Level.query.filter(Level.level==level_name).first()
    
    assert level.description == '거예요, 아서, 러'

# E_GroupManager
def test_add_e_group(app):
    level = 1
    e_group_name = "ハムニダ用言、助詞、否定"
    description = "갑니다,에서,지 않다"
    position = None
    with app.app_context():
        editor.E_GroupManager.add_e_group(level, e_group_name, description, position)
        e_group = E_Group.query.filter(E_Group.e_group==e_group_name).first()

    assert e_group.description == '갑니다,에서,지 않다'

# ElementManager
def test_add_element(app):
    e_group = 1
    element_name = '指示詞の否定'
    description = '아닙니다'
    position = None
    with app.app_context():
        editor.ElementManager.add_element(e_group, element_name, description, position)
        element = Element.query.filter(Element.element==element_name).first()

    assert element.description == '아닙니다'

# QuestionManager
def test_add_question(app):
    element = 1
    japanese = '私は学生です。'
    foreign_l = '저는 학생입니다.'
    style = 1
    position = None
    user = 1
    with app.app_context():
        editor.QuestionManager.add_question(element, japanese, foreign_l, style, position, user)
        question = Question.query.filter(Question.japanese==japanese).first()

    assert question.foreign_l == '저는 학생입니다.'

def test_fetch_questions_with_hints(app):
    element = 1
    with app.app_context():
        questions = editor.QuestionManager.fetch_questions_with_hints(element)
    
    assert questions[0]['hint'][0].japanese == '医者'

def test_fetch_question_with_hints(app):
    question = 1
    with app.app_context():
        question = editor.QuestionManager.fetch_question_with_hints(question)

    assert question['word'][0] == '父'

#WordManager
def test_add_word(app):
    j_word = '父'
    f_word = '아버지'
    with app.app_context():
        editor.WordManager.add_word(j_word, f_word)
        word = Word.query.filter(Word.japanese==j_word).filter(Word.foreign_l==f_word).first()
    assert word.foreign_l == '아버지'

#HintManager  
def test_fetch_word(app):
    question = 1
    word = 1
    with app.app_context():
        words = editor.HintManager.fetch_word(question)
    
    assert words[0].japanese == '医者'

def test_confirm_j_hint(app):
    question = 1
    j_word = '医者'
    with app.app_context():
        existed = editor.HintManager.confirm_j_hint(question, j_word)

    assert existed == 1

def test_confirm_f_hint(app):
    question = 1
    f_word = '의사'
    with app.app_context():
        existed = editor.HintManager.confirm_f_hint(question, f_word)

    assert existed == 1

def test_add_hint(app):
    question = 1
    word = 1
    with app.app_context():
        editor.HintManager.add_hint(question, word)
        hint = Hint.query.filter(Hint.question==1).first()
    
    assert hint.word == 1





