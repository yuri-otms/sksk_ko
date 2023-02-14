from flask import Blueprint, redirect, url_for, render_template, request, \
    flash, session
from flask_login import login_required
from sqlalchemy import func

from sksk_app import db
from sksk_app.models import Level, E_Group
from sksk_app.utils.edit import LevelManager, E_GroupManager

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

@edit.route('/show')
@login_required
def show():
    levels = db.session.query(Level).all()
    e_groups_raw = db.session.query(E_Group).all()
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
    return render_template('edit/show.html', levels = levels, e_groups=e_groups)

@edit.route('/add/level', methods=['POST'])
@login_required
def add_level():
    level = request.form['level_name']
    description = request.form['level_desc']

    LevelManager.add_level(level, description)

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

    E_GroupManager.add_e_group(level_id, e_group, description, position)
    # new_e_group = E_Group(
    #     level = 1,
    #     e_group = '指示詞',
    #     description = '説明',
    #     position = 1
    # )
        
    # db.session.add(new_e_group)
    # db.session.commit()

    return redirect(url_for('edit.add_e_group_done'))

@edit.route('/add/e_group_added_done')
@login_required
def add_e_group_done():
    flash('項目グループを登録しました')
    return redirect(url_for('edit.show'))