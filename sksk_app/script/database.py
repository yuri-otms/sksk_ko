# from flask.cli import with_appcontext
from flask import Flask
from flask import Blueprint

from sksk_app import db
from sksk_app.models import User, Grade, Process, Level
import sksk_app.utils.user as user_setting
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
    grade = 'ハン検5級'
    description = '입니다, 고 싶다, ㄹ까요'
    position = 1
    editor.GradeManager.add_grade(grade, description,position)


    name = 'test'
    email = 'test@test.com'
    password = '1234'
    user_setting.UserManager.register_user(name, email, password)
    user_setting.UserManager.add_privilege(1, 1)
    user_setting.UserManager.add_privilege(1, 2)
    user_setting.UserManager.add_privilege(1, 3)
    user_setting.UserManager.add_privilege(1, 4)

    user_setting.UserManager.register_process()

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

    grade = 1
    e_group = '指示詞、存在詞、数詞'
    description = '입니다, 있다, 하나'
    position = 1
    editor.E_GroupManager.add_e_group(grade, e_group, description, position)

    e_group = 1
    element = '指示詞'
    description = '입니다'
    position = 1
    editor.ElementManager.add_element(e_group, element, description, position)

    new_level = Level(
        level = 1
    )
    db.session.add(new_level)
    db.session.commit()

    element = 1
    level = 1
    japanese = '父は医者です。'
    foreign_l = '아버지는 의사입니다.'
    style = 1
    position = None
    user = 1
    editor.QuestionManager.add_question(element, level , japanese, foreign_l, style, position, user)

    # element = 1
    # japanese = '私は学生です。'
    # foreign_l = '저는 학생입니다.'
    # style = 1
    # position = None
    # user = 1
    # editor.QuestionManager.add_question(element, japanese, foreign_l, style, position, user)


    # element = 1
    # japanese = '母は公務員です。'
    # foreign_l = '어머니는 공무원입니다.'
    # style = 1
    # position = None
    # user = 1
    # editor.QuestionManager.add_question(element, japanese, foreign_l, style, position, user)

    # question = 1
    # word = 1
    # editor.HintManager.add_hint(question, word)


    print("Insert User Data ")

@qtdb.cli.command('temp')
def delete_grade():
    grade = 1
    e_group = '指示詞、存在詞、数詞'
    description = '입니다, 있다, 하나'
    position = 1
    editor.E_GroupManager.add_e_group(grade, e_group, description, position)
    # user = db.session.get(User, 1)
    # user.check = False
    # db.session.merge(user)
    # db.session.commit()
    print("Execute temp")
