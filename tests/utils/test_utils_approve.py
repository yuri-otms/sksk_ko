from sksk_app import db
from sksk_app.models import Level, E_Group, Element, Question
import sksk_app.utils.approve as approval

def test_change_level_settings(app):
    with app.app_context():
        approval.ReleaseManager.change_level_settings(1)
        level = db.session.get(Level, 1)

    assert level.released == True


def test_change_e_group_settings(app):
    with app.app_context():
        approval.ReleaseManager.change_e_group_settings(1)
        e_group = db.session.get(E_Group, 1)

    assert e_group.released == True

def test_change_element_settings(app):
    with app.app_context():
        approval.ReleaseManager.change_element_settings(1)
        element = db.session.get(Element, 1)

    assert element.released == True

def test_change_question_settings(app):
    with app.app_context():
        approval.ReleaseManager.change_question_settings(1)
        question = db.session.get(Question, 1)

    assert question.released == True

def test_release_questions(app):
    questions = [1, 2]
    with app.app_context():
        approval.ReleaseManager.release_questions(questions)
        questions = Question.query.all()

    assert questions[0].released == True
    assert questions[2].released == False

def test_release_questions(app):
    # 一度公開設定にし、その後に非公開にする
    questions = [1, 2, 3]
    with app.app_context():
        approval.ReleaseManager.release_questions(questions)
        questions = [1, 2]
        approval.ReleaseManager.unrelease_questions(questions)

        questions = Question.query.all()


    assert questions[0].released == False
    assert questions[2].released == True


