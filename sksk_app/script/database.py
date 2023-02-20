# from flask.cli import with_appcontext
from flask import Flask
from flask import Blueprint

from sksk_app import db
from sksk_app.models import User, Level, Process
from sksk_app.utils.questions import QuestionManager
from sksk_app.utils.auth import UserManager
import sksk_app.utils.edit as editor

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
    description = '입니다, 고 싶다, ㄹ까요'
    QuestionManager.insert_level(level,None,None)

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

    level = 1
    e_group = '指示詞、存在詞、数詞'
    description = '입니다, 있다, 하나'
    position = 1
    editor.E_GroupManager.add_e_group(level, e_group, description, position)

    e_group = 1
    element = '指示詞'
    description = '입니다'
    position = 1
    editor.ElementManager.add_element(e_group, element, description, position)
    QuestionManager.delete_testing_levels()
    
    name = 'test'
    email = 'test@test.com'
    password = '1234'
    UserManager.register_user(name, email, password)
    UserManager.add_privilege(1, 1)
    UserManager.add_privilege(1, 2)
    UserManager.add_privilege(1, 3)
    UserManager.add_privilege(1, 4)

    UserManager.register_process()

    print("Insert User Data ")

@qtdb.cli.command('temp')
def delete_level():
    level = 1
    e_group = '指示詞、存在詞、数詞'
    description = '입니다, 있다, 하나'
    position = 1
    editor.E_GroupManager.add_e_group(level, e_group, description, position)
    # user = db.session.get(User, 1)
    # user.check = False
    # db.session.merge(user)
    # db.session.commit()
    print("Execute temp")

@qtdb.cli.command('add_element')
def delete_level():
    e_group = 1
    element = '指示詞'
    description = '입니다'
    position = 1
    editor.ElementManager.add_e_group(e_group, element, description, position)
    QuestionManager.delete_testing_levels()

    print("Delete Levels")

@qtdb.cli.command('delete_level')
def delete_level():
    QuestionManager.delete_testing_levels()

    print("Delete Levels")