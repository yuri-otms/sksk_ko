from sksk_app import db
from sksk_app.models import Grade, E_Group, Element, Question
import sksk_app.utils.approve as approval

def test_change_question_settings(app):
    user = 1
    with app.app_context():
        approval.ReleaseManager.change_question_settings(user,1)
        question = db.session.get(Question, 1)

    assert question.released == True

def test_release_questions(app):
    user = 1
    questions = [1, 2]
    with app.app_context():
        approval.ReleaseManager.release_questions(user, questions)
        questions = Question.query.all()

    assert questions[0].released == True
    assert questions[2].released == False

def test_unrelease_questions(app):
    # 一度公開設定にし、その後に非公開にする
    user = 1
    questions = [1, 2, 3]
    with app.app_context():
        approval.ReleaseManager.release_questions(user, questions)
        questions = [1, 2]
        approval.ReleaseManager.unrelease_questions(user, questions)

        questions = Question.query.all()


    assert questions[0].released == False
    assert questions[2].released == True


