from app import db
from models.grade import Grade
from models.e_group import E_Group
from models.element import Element
from models.question import Question

import app.utils.approve as approval

def test_change_question_settings(app):
    user = 1
    with app.app_context():
        approval.ReleaseManager.change_question_settings(user,1)
        question = db.session.get(Question, 1)

    assert question.process == 8

def test_release_questions(app):
    user = 1
    questions = [1, 2]
    with app.app_context():
        approval.ReleaseManager.release_questions(user, questions)
        questions = Question.query.all()

    assert questions[0].process == 8
    assert questions[2].process != 8

def test_unrelease_questions(app):
    # 一度公開設定にし、その後に非公開にする
    user = 1
    questions = [1, 2, 3]
    with app.app_context():
        approval.ReleaseManager.release_questions(user, questions)
        questions = [1, 2]
        approval.ReleaseManager.unrelease_questions(user, questions)

        questions = Question.query.all()


    assert questions[0].process == 9
    assert questions[2].process == 8


