# from flask.cli import with_appcontext
from flask import Flask
from flask import Blueprint
from werkzeug.security import generate_password_hash
from datetime import datetime

from sksk_app import db
from sksk_app.models import User, Level
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
    
    new_user = Level(
    level = level
    )
    
    db.session.add(new_user)
    db.session.commit()
    
    name = 'test'
    email = 'test@test.com'
    password = '1234'
    UserManager.register_user(name, email, password)

    name = 'testE'
    email = 'testE@test.com'
    password = '1234'
    edit = 1
    UserManager.register_user(name, email, password)

    print("Insert User Data ")

@qtdb.cli.command('delete_level')
def delete_level():
    QuestionManager.delete_testing_levels()

    print("Delete Levels")