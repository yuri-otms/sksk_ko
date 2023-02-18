from flask import Blueprint, redirect, url_for, render_template, request, \
    flash, session
from flask_login import login_required
from sqlalchemy import func

from sksk_app import db
from sksk_app.models import Level, E_Group, Element, Style, Question
import sksk_app.utils.edit as editor

edit = Blueprint('edit', __name__, url_prefix='/edit')

@edit.before_request
def load_logged_in_user():
    edit = session.get('edit')

    if not edit:
        flash('アクセスが許可されていません')
        return redirect(url_for('pg.toppage'))

@edit.route('/index')
@login_required
def index():
    level_id = editor.EditManager.fetchLevel()
    level = db.session.get(Level, level_id)
    level_position = level.position
    levels = Level.query.all()
    e_groups = E_Group.query.filter(E_Group.level==level_id)
    return render_template('edit/index.html', level_id=level_id, levels=levels, e_groups=e_groups, level_position=level_position)

@edit.route('/show', methods=['GET'])
@login_required
def show():
    #選択された項目グループの項目を表示
    level_id = editor.EditManager.fetchLevel()
    e_group_id = editor.EditManager.fetchE_Group(level_id)

    levels = db.session.query(Level).all()
    e_groups = editor.EditManager.addE_GroupName(level_id)

    e_group = db.session.get(E_Group, e_group_id)
    level_id = e_group.level
    level = db.session.get(Level, level_id)
    level_name = level.level
    level_position = level.position
    elements = Element.query.filter(Element.e_group==e_group_id)
    e_group_name = e_group.e_group
    e_group_position = e_group.position
    e_group_id = e_group.id


    return render_template('edit/show.html', levels = levels, e_groups=e_groups, elements=elements,level_name=level_name, level_id=level_id, level_position = level_position,e_group_position=e_group_position,e_group_name=e_group_name, e_group_id=e_group_id)

@edit.route('/show/questions', methods=['GET'])
def show_questions():
    if request.args.get('l'):
        level_id = editor.EditManager.fetchLevel()
        e_group_id = editor.EditManager.fetchE_Group(level_id)
        element_id = editor.EditManager.fetchElement(e_group_id)
    elif request.args.get('g'):
        e_group_id = request.args.get('g')
        level_id = db.session.get(E_Group, e_group_id).level
        element_id = editor.EditManager.fetchElement(e_group_id)
    elif request.args.get('e'):
        element_id = request.args.get('e')
        e_group_id = db.session.get(Element, element_id).e_group
        level_id = db.session.get(E_Group, e_group_id).level
    else:
        level_id = editor.EditManager.fetchLevel()
        e_group_id = editor.EditManager.fetchE_Group(level_id)
        element_id = editor.EditManager.fetchElement(e_group_id)
        
    element = db.session.get(Element, element_id)

    level = db.session.get(Level, level_id)
    level_position = level.position

    e_group_id = editor.EditManager.fetchE_Group(level_id)
    e_group_position = db.session.get(E_Group, e_group_id).position
    levels = Level.query.all()
    e_groups = E_Group.query.filter(E_Group.level==level_id)
    styles = Style.query.all()

    elements = Element.query.filter(Element.e_group==e_group_id)

    questions_raw = Question.query.filter(Question.element==element.id)
    questions = []
    for question in questions_raw:
        style = db.session.get(Style, question.style)
        one_question = {
            "id":question.id,
            "japanese":question.japanese,
            "foreign_l":question.foreign_l,
            "style": style.style,
            "position":question.position
        }
        questions.append(one_question)

    return render_template('edit/show_questions.html',level_id=level_id, level_position= level_position, e_group_position=e_group_position, levels=levels, e_groups=e_groups, styles=styles, e_group_id=e_group_id, elements=elements, element=element, questions=questions)


@edit.route('/add/level', methods=['POST'])
@login_required
def add_level():
    level_name = request.form['level']
    description = request.form['description']
    position = request.form['position']

    level = Level(
        level = level_name,
        description = description,
        position = position
    
    )

    return render_template('edit/add_level.html', level = level)


@edit.route('/add/level_added', methods=['POST'])
@login_required
def add_level_execute():
    level = request.form['level']
    description = request.form['description']
    position = request.form['position']
    editor.LevelManager.add_level(level, description, position)
    # レベルを追加すると同時にグループを1つ追加する。
    level_id = Level.query.filter(Level.level== level).first().id
    e_group = '新規グループ'
    description = '新規グループ'
    position = 1
    editor.E_GroupManager.add_e_group(level_id, e_group, description, position)
    # 項目グループを追加すると同時に項目を1つ追加する。
    e_group_id = E_Group.query.filter(E_Group.e_group==e_group).first().id
    element = '新規項目'
    description = '新規項目'
    position = 1
    editor.ElementManager.add_element(e_group_id, element, description, position)
    

    return redirect(url_for('edit.add_level_done'))



@edit.route('/add/level/done')
@login_required
def add_level_done():
    flash('レベルを登録を行いました。')

    return redirect(url_for('edit.show'))

@edit.route('/add/e_group', methods=['POST'])
@login_required
def add_e_group():
    level_id = request.form['level']
    e_group = request.form['e_group_name']
    description = request.form['description']
    position = request.form['position']

    level = db.session.get(Level, level_id)
    e_group = E_Group(
        level = level,
        e_group = e_group,
        description = description,
        position = position
    )

    return render_template('edit/add_e_group.html', e_group=e_group, level_name=level.level)

@edit.route('/add/e_groupe_added', methods=['POST'])
@login_required
def add_e_group_execute():
    level_id = request.form['level']
    e_group = request.form['e_group']
    description = request.form['description']
    position = request.form['position']

    editor.E_GroupManager.add_e_group(level_id, e_group, description, position)
    # 項目グループを追加すると同時に項目を1つ追加する。
    e_group_id = E_Group.query.filter(E_Group.e_group==e_group).first().id
    element = '項目1'
    description = '一つ目の項目'
    position = 1
    editor.ElementManager.add_element(e_group_id, element, description, position)

    return redirect(url_for('edit.add_e_group_done', l=level_id))

@edit.route('/add/e_group_added_done')
@login_required
def add_e_group_done():
    level_id = request.args.get('l')
    flash('項目グループを登録しました')
    return redirect(url_for('edit.show', l=level_id))


# 項目の追加
@edit.route('/add/element', methods=['POST'])
@login_required
def add_element():
    e_group_id = request.form['e_group_id']
    element_name = request.form['element_name']
    description = request.form['description']
    position = request.form['position']

    e_group = db.session.get(E_Group, e_group_id)
    e_group_name=e_group.e_group
    element = Element(
        e_group = e_group_id,
        element = element_name,
        description = description,
        position = position
    )

    return render_template('edit/add_element.html', element=element, e_group_name=e_group_name)

@edit.route('/add/element_added', methods=['POST'])
@login_required
def add_element_execute():
    e_group_id = request.form['e_group']
    element_name= request.form['element_name']
    description = request.form['description']
    position = request.form['position']

    editor.ElementManager.add_element(e_group_id, element_name, description, position)

    level_id = db.session.get(E_Group, e_group_id).level

    return redirect(url_for('edit.add_element_done', l=level_id, g=e_group_id))

@edit.route('/add/element_added_done')
@login_required
def add_element_done():
    level_id = request.args.get('l')
    e_group_id = request.args.get('g')
    flash('項目を登録しました')
    return redirect(url_for('edit.show', l=level_id, g=e_group_id))

@edit.route('/add/question', methods=['POST'])
@login_required
def add_question():
    japanese = request.form['japanese1']
    foreign_l = request.form['foreign_l1']
    style_id = request.form['style']
    position = request.form['position']
    element_id = request.form['element_id']

    style = db.session.get(Style, style_id)
    element = db.session.get(Element, element_id)
    e_group = db.session.get(E_Group, element.e_group)
    level = db.session.get(Level, e_group.level)

    question = {
        "level":level.level,
        "e_group":e_group.e_group,
        "element_id":element.id,
        "element": element.element,
        "japanese": japanese,
        "foreign_l": foreign_l,
        "style_id": style.id,
        "style":style.style,
        "position": position,
    }

    return render_template('edit/add_question.html', question=question)

@edit.route('/add/question_added', methods=['POST'])
@login_required
def add_question_execute():
    element = request.form['element']
    japanese1 = request.form['japanese1']
    foreign_l1 = request.form['foreign_l1']
    style = request.form['style']
    position = request.form['position']

    editor.QuestionManager.add_question(element, japanese1, foreign_l1, style, position)

    return redirect(url_for('edit.add_question_done', e=element))

@edit.route('/add/question_added_done')
@login_required
def add_question_done():
    element = request.args.get('e')
    flash('問題文を追加しました。')

    return redirect(url_for('edit.show_questions', e=element))

