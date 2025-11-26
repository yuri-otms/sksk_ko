from app import db
from app.models import Grade, E_Group, Element, Question, Word, Hint
import app.utils.edit as editor

# gradeManager
def test_add_grade(app):
    grade_name = 'ハン検4級'
    description = '거예요, 아서, 러'
    with app.app_context():
        editor.GradeManager.add_grade(grade_name,description)
        grade = Grade.query.filter(Grade.grade==grade_name).first()
    
    assert grade.description == '거예요, 아서, 러'

def test_edit_grade(app):
    grade_name = 'ハン検4級'
    description = '거예요, 아서, 러'
    with app.app_context():
        editor.GradeManager.add_grade(grade_name,description)
        grade = Grade.query.filter(Grade.grade==grade_name).first()
        description = '거예요'
        editor.GradeManager.edit_grade(grade.id, grade_name, description)
        grade = db.session.get(Grade,grade.id)

    assert grade.description == '거예요'

def test_delete_grade(app):
    grade_name = 'ハン検4級'
    description = '거예요, 아서, 러'
    with app.app_context():
        editor.GradeManager.add_grade(grade_name,description)
        grade = Grade.query.filter(Grade.grade==grade_name).first()
        editor.GradeManager.delete_grade(grade.id)
        grade = db.session.get(Grade, grade.id)

    assert grade is None

# E_GroupManager
def test_add_e_group(app):
    grade = 1
    e_group_name = "ハムニダ用言、助詞、否定"
    description = "갑니다,에서,지 않다"
    position = None
    with app.app_context():
        editor.E_GroupManager.add_e_group(grade, e_group_name, description)
        e_group = E_Group.query.filter(E_Group.e_group==e_group_name).first()

    assert e_group.description == '갑니다,에서,지 않다'

# ElementManager
def test_add_element(app):
    e_group = 1
    element_name = '指示詞の否定'
    description = '아닙니다'
    with app.app_context():
        editor.ElementManager.add_element(e_group, element_name, description)
        element = Element.query.filter(Element.element==element_name).first()

    assert element.description == '아닙니다'

# QuestionManager
def test_add_question(app):
    element = 1
    level = 1
    japanese = '私のカバンですか？'
    foreign_l = '제 가방입니까?'
    style = 1
    spoken = 0
    sida = 0
    will = 0
    user = 1
    with app.app_context():
        editor.QuestionManager.add_question(element, level, japanese, foreign_l, style, spoken, sida, will, user)
        question = Question.query.filter(Question.japanese==japanese).first()

    assert question.foreign_l == '제 가방입니까?'

def test_edit_question(app):
    element = 1
    level = 1
    japanese = '私のカバンですか？'
    foreign_l = '제 가방입니까?'
    style = 1
    spoken = 0
    sida = 0
    will = 0
    user = 1
    with app.app_context():
        editor.QuestionManager.add_question(element, level, japanese, foreign_l, style, spoken, sida, will, user)
        question = Question.query.filter(Question.japanese==japanese).first()
        foreign_l = '제 가방이에요?'
        style = 2
        editor.QuestionManager.edit_question(question.id, element, japanese, foreign_l, style, spoken, sida, will,user, 0)
        question = db.session.get(Question, question.id)
    
    assert question.foreign_l == '제 가방이에요?'

def test_delete_question(app):
    with app.app_context():
        user = 1
        element = 1
        level = 1
        japanese = '私のカバンですか？'
        foreign_l = '제 가방입니까?'
        style = 1
        spoken = 0
        sida = 0
        will = 0
        user = 1
        editor.QuestionManager.add_question(element, level, japanese, foreign_l, style, spoken, sida, will, user)
        japanese = 'これはキムチですか？'
        foreign_l = '이것은 김치입니까?'
        editor.QuestionManager.add_question(element, level, japanese, foreign_l, style, spoken, sida, will, user)
        japanese = '今日は休日ではありません。'
        foreign_l = '오늘은 휴일이 아닙니다.'
        editor.QuestionManager.add_question(element, level, japanese, foreign_l, style, spoken, sida, will, user)

        question1 = Question.query.filter(Question.japanese=="私のカバンですか？").first()
        question2 = Question.query.filter(Question.japanese=="今日は休日ではありません。").first()
        position = question2.position
        editor.QuestionManager.delete_question(question1.id, user)
        question2_edited = Question.query.filter(Question.japanese=="今日は休日ではありません。").first()

        assert question2_edited.position == position - 1

def test_fetch_questions_with_hints(app):
    element = 1
    with app.app_context():
        questions = editor.QuestionManager.fetch_questions_with_hints(element)
    
    assert questions[0]['hint'][0].japanese == '医者'

def test_fetch_question_with_components_hints(app):
    question = 1
    with app.app_context():
        question = editor.QuestionManager.fetch_question_with_components_hints(question)

    assert question['japanese_word'][0] == '父'

def test_fetch_question_with_hints(app):
    question = 1
    with app.app_context():
        question = editor.QuestionManager.fetch_question_with_hints(question)
    
    assert question['hint'][0].foreign_l == '의사'

def test_fetch_attribute(app):
    element = 1
    with app.app_context():
        attribute = editor.QuestionManager.fetch_attribute(element)
    assert attribute['description'] == '입니다'
        


#WordManager
def test_add_word(app):
    japanese_word = '父'
    foreign_word = '아버지'
    with app.app_context():
        editor.WordManager.add_word(japanese_word, foreign_word)
        word = Word.query.filter(Word.japanese==japanese_word).filter(Word.foreign_l==foreign_word).first()
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





