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
    editor.GradeManager.add_grade(grade, description)

    user_setting.UserManager.register_privilege()
    user_setting.UserManager.register_process()

    name = 'test'
    email = 'test@test.com'
    password = '1234'
    user_setting.UserManager.register_user(name, email, password)
    user_setting.UserManager.add_privilege(1, 1)
    user_setting.UserManager.add_privilege(1, 2)
    user_setting.UserManager.add_privilege(1, 3)
    user_setting.UserManager.add_privilege(1, 4)

    name = 'editor'
    email = 'editor@test.com'
    password = '1234'
    user_setting.UserManager.register_user(name, email, password)
    user_setting.UserManager.add_privilege(2, 1)

    name = 'checker'
    email = 'checker@test.com'
    password = '1234'
    user_setting.UserManager.register_user(name, email, password)
    user_setting.UserManager.add_privilege(3, 2)

    name = 'approver'
    email = 'approver@test.com'
    password = '1234'
    user_setting.UserManager.register_user(name, email, password)
    user_setting.UserManager.add_privilege(4, 3)

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
    editor.E_GroupManager.add_e_group(grade, e_group, description)

    e_group = 1
    element = '指示詞'
    description = '입니다'
    editor.ElementManager.add_element(e_group, element, description)

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
    spoken = 0
    sida = 0
    will = 0
    user = 2
    editor.QuestionManager.add_question(element, level , japanese, foreign_l, style, spoken, sida, will, user)

    japanese = '私は学生です。'
    foreign_l = '저는 학생입니다.'
    editor.QuestionManager.add_question(element, level , japanese, foreign_l, style, spoken, sida, will, user)

    japanese = '母は公務員です。'
    foreign_l = '어머니는 공무원입니다.'
    editor.QuestionManager.add_question(element, level , japanese, foreign_l, style, spoken, sida, will, user)

    japanese = '私のカバンですか？'
    foreign_l = '제 가방입니까?'
    editor.QuestionManager.add_question(element, level , japanese, foreign_l, style, spoken, sida, will, user)

    japanese = 'これはキムチですか？'
    foreign_l = '이것은 김치입니까?'
    editor.QuestionManager.add_question(element, level , japanese, foreign_l, style, spoken, sida, will, user)

    print("Insert User Data ")

@qtdb.cli.command('add')
def delete_grade():

    e_group = 1
    element = '指示詞の否定'
    description = '아닙니다'
    editor.ElementManager.add_element(e_group, element, description)

    element = 2
    level = 1
    japanese = '今日は休日ではありません。'
    foreign_l = '오늘은 휴일이 아닙니다.'
    style = 1
    spoken = 0
    sida = 0
    will = 0
    user = 2
    editor.QuestionManager.add_question(element, level , japanese, foreign_l, style, spoken, sida, will, user)
    japanese = 'ここは銀行ではありません。'
    foreign_l = '여기는 은행이 아닙니다.'
    editor.QuestionManager.add_question(element, level , japanese, foreign_l, style, spoken, sida, will, user)
    japanese = '風邪ではありませんか？'
    foreign_l = '감기가 아닙니까?'
    editor.QuestionManager.add_question(element, level , japanese, foreign_l, style, spoken, sida, will, user)
    japanese = '私のノートではありません。'
    foreign_l = '제 노트가 아닙니다.'
    editor.QuestionManager.add_question(element, level , japanese, foreign_l, style, spoken, sida, will, user)
    japanese = '弟ではありません。'
    foreign_l = '남동생이 아닙니다.'
    editor.QuestionManager.add_question(element, level , japanese, foreign_l, style, spoken, sida, will, user)


    e_group = 1
    element = '存在詞'
    description = '았다, 없다'
    editor.ElementManager.add_element(e_group, element, description)

    element = 3
    level = 1
    japanese = '宿題があります。'
    foreign_l = '숙제가 있습니다.'
    style = 1
    spoken = 0
    sida = 0
    will = 0
    user = 2
    editor.QuestionManager.add_question(element, level , japanese, foreign_l, style, spoken, sida, will, user)
    japanese = '火曜日に試験があります。'
    foreign_l = '화요일에 시험이 있습니다.'
    editor.QuestionManager.add_question(element, level , japanese, foreign_l, style, spoken, sida, will, user)
    japanese = '姉と妹がいます。'
    foreign_l = '언니하고 여동생이 있습니다.'
    editor.QuestionManager.add_question(element, level , japanese, foreign_l, style, spoken, sida, will, user)
    japanese = '日曜日は授業がありませんか？'
    foreign_l = '일요일은 수업이 없습니까?'
    editor.QuestionManager.add_question(element, level , japanese, foreign_l, style, spoken, sida, will, user)
    japanese = '母は家にいません。'
    foreign_l = '어머니는 집에 없습니다.'
    editor.QuestionManager.add_question(element, level , japanese, foreign_l, style, spoken, sida, will, user)



    # e_group = 1
    # element = ''
    # description = ''
    # editor.ElementManager.add_element(e_group, element, description)

    # element = 
    # level = 1
    # japanese = ''
    # foreign_l = ''
    # style = 1
    # spoken = 0
    # sida = 0
    # will = 0
    # user = 2
    # editor.QuestionManager.add_question(element, level , japanese, foreign_l, style, spoken, sida, will, user)
    # japanese = ''
    # foreign_l = ''
    # editor.QuestionManager.add_question(element, level , japanese, foreign_l, style, spoken, sida, will, user)
    # japanese = ''
    # foreign_l = ''
    # editor.QuestionManager.add_question(element, level , japanese, foreign_l, style, spoken, sida, will, user)
    # japanese = ''
    # foreign_l = ''
    # editor.QuestionManager.add_question(element, level , japanese, foreign_l, style, spoken, sida, will, user)
    # japanese = ''
    # foreign_l = ''
    # editor.QuestionManager.add_question(element, level , japanese, foreign_l, style, spoken, sida, will, user)
    print("Execute temp")
