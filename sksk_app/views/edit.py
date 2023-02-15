from flask import Blueprint, redirect, url_for, render_template, request, \
    flash, session
from flask_login import login_required
from sqlalchemy import func

from sksk_app import db
from sksk_app.models import Level, E_Group, Element
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
    return render_template('edit/index.html')

@edit.route('/show', methods=['GET'])
@login_required
def show():
    levels = db.session.query(Level).all()
    e_groups_raw = db.session.query(E_Group).all()
    # 項目グループの名称を追加
    e_groups = []
    for e_group in e_groups_raw:
        level_name = db.session.get(Level, e_group.level)
        e_group_added = {
            "id":e_group.id,
            "level":e_group.level,
            "level_name":level_name.level,
            "e_group":e_group.e_group,
            "description":e_group.description,
            "position":e_group.position,
            "released":e_group.released
        }
        e_groups.append(e_group_added)
    #選択された項目グループの項目を表示
    if request.args.get('g'):
        e_group_id = request.args.get('g')
    else:
        e_group = E_Group.query.with_entities(E_Group.level, func.min(E_Group.id).label('e_group_min')).filter(E_Group.level==1).group_by(E_Group.level).one()
        e_group_id = e_group.e_group_min
    e_group = db.session.get(E_Group, e_group_id)
    level = db.session.get(Level, e_group.level)
    elements = Element.query.filter(Element.e_group==e_group_id)
    level_name = level.level
    e_group_name = e_group.e_group
    

    return render_template('edit/show.html', levels = levels, e_groups=e_groups, elements=elements,level_name=level_name, e_group_name=e_group_name)

@edit.route('/add/level', methods=['POST'])
@login_required
def add_level():
    level = request.form['level_name']
    description = request.form['level_desc']
    position = request.form['position']
    editor.LevelManager.add_level(level, description, position)

    return redirect(url_for('edit.add_level_done'))

@edit.route('/add/level/done')
@login_required
def add_level_done():
    flash('ユーザー登録を行いました。')

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

    return redirect(url_for('edit.add_e_group_done'))

@edit.route('/add/e_group_added_done')
@login_required
def add_e_group_done():
    flash('項目グループを登録しました')
    return redirect(url_for('edit.show'))


# 項目の追加
@edit.route('/add/element', methods=['POST'])
@login_required
def add_element():
    e_group_id = request.form['e_group_id']
    element_name = request.form['element_name']
    description = request.form['description']
    position = request.form['position']

    e_group = db.session.get(E_Group, e_group_id)
    element = Element(
        e_group = e_group,
        element = element_name,
        description = description,
        position = position
    )

    return render_template('edit/add_element.html', element=element)

@edit.route('/add/element_added', methods=['POST'])
@login_required
def add_element_execute():
    e_group_id = request.form['e_group']
    element_name= request.form['element_name']
    description = request.form['description']
    position = request.form['position']

    editor.ElementManager.add_element(e_group_id, element_name, description, position)


    return redirect(url_for('edit.add_element_done'))

@edit.route('/add/element_added_done')
@login_required
def add_element_done():
    flash('項目を登録しました')
    return redirect(url_for('edit.show'))
