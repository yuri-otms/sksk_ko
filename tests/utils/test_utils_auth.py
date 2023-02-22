from sksk_app import db
from sksk_app.models import User, Process, Score
import sksk_app.utils.auth as auth

TEST_NAME = 'test99'
TEST_EMAIL = 'test99@test.com'

def register_test_user(app):
    name = 'test99'
    email = 'test99@test.com'
    password = '1234'
    with app.app_context():
        auth.UserManager.register_user(name, email, password)


def test_register_user(app):
    name = 'test99'
    email = 'test99@test.com'
    password = '1234'
    with app.app_context():
        auth.UserManager.register_user(name, email, password)
        user = User.query.filter(User.email==email).first()

    assert user.name == name

def test_register_user_priv(app):
    name = 'test_priv'
    email = 'test_priv@test.com'
    password = '1345'
    edit = 1
    check = 0
    approve = 1
    admin = 0
    with app.app_context():
        auth.UserManager.register_user_priv(name, email,  password, edit, check, approve, admin)
        user = User.query.filter(User.email==email).first()

    assert user.edit == True
    assert user.check == False
    assert user.approve == True
    assert user.admin == False

def test_delete_user(app):
    with app.app_context():
        register_test_user(app)
        user = User.query.filter(User.name==TEST_NAME).first()
        auth.UserManager.delete_user(user.id)
        user = User.query.filter(User.name==TEST_NAME).first()

    assert user is None


def test_edit_user(app):
    with app.app_context():
        register_test_user(app)
        user = User.query.filter(User.name==TEST_NAME).first()
        auth.UserManager.edit_user(user.id, "test98", "test98@test.com", 0,1,0,1)
        user = User.query.filter(User.id==user.id).first()

    assert user.name == "test98"
    assert user.email ==  "test98@test.com"


def test_add_privilege(app):
    with app.app_context():
        register_test_user(app)
        user = User.query.filter(User.name==TEST_NAME).first()
        auth.UserManager.add_privilege(user.id, 1)
        user = User.query.filter(User.name==TEST_NAME).first()

    assert user.edit == True

def test_delete_privilege(app):
    with app.app_context():
        register_test_user(app)
        user = User.query.filter(User.name==TEST_NAME).first()
        auth.UserManager.add_privilege(user.id, 1)
        user = User.query.filter(User.name==TEST_NAME).first()

    assert user.edit == True

    with app.app_context():
        auth.UserManager.delete_privilege(user.id, 1)
        user = User.query.filter(User.name==TEST_NAME).first()

    assert user.edit == False

def test_register_process(app):
    with app.app_context():
        auth.UserManager.register_process()
        processes = Process.query.all()
        processes_name = ['編集', '確認', '承認', '管理']
        for process in processes:
            assert process.process == processes_name[process.id - 1]

# ScoreManager
def test_add_score(app):
    user = 1
    question = 1
    correct = 1
    review = 0
    with app.app_context():
        auth.ScoreManager.add_score(user, question, correct, review)
        score = Score.query.filter(Score.user==1).filter(Score.question==1).first()

    assert score.correct == 1










