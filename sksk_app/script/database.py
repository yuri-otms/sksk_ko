# from flask.cli import with_appcontext
from flask import Flask
from flask import Blueprint

from sksk_app import db
from sksk_app.models import User, Level, Process
from sksk_app.utils.questions import QuestionManager
from sksk_app.utils.auth import UserManager

app = Flask(__name__)

qtdb = Blueprint('create', __name__)

# コマンド機能の作成
@qtdb.cli.command('all')
def create():
    db.create_all()
    print("Create All Tables ")

app.cli.add_command(create)

@qtdb.cli.command('init')
def init():
    level = 'ハン検5級'
    
    QuestionManager.insert_level(level,None,None)
    
    name = 'test'
    email = 'test@test.com'
    password = '1234'
    UserManager.register_user(name, email, password)
    UserManager.add_privilege(1, 1)
    UserManager.add_privilege(1, 4)

    print("Insert User Data ")

    UserManager.register_process()

@qtdb.cli.command('temp')
def delete_level():
    user = db.session.get(User, 1)
    user.check = False
    db.session.merge(user)
    db.session.commit()
    print("Execute temp")

@qtdb.cli.command('delete_level')
def delete_level():
    QuestionManager.delete_testing_levels()

    print("Delete Levels")