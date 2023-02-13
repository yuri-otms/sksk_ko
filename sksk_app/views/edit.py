from flask import Blueprint, redirect, url_for, render_template, request, \
    flash, session
from flask_login import login_required
from sqlalchemy import func

from sksk_app import db
from sksk_app.models import Level

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
    return render_template('edit/show.html', levels = levels)

@edit.route('/add/level', methods=['POST'])
@login_required
def add_level():
    level = request.form['level_name']
    description = request.form['level_desc']

    max_position = db.session.query(
        func.max(Level.position).label('level_max')).one()
    max = int(max_position.level_max)

    position = max + 1

    new_level = Level(
        level = level,
        description = description,
        position = position
    )
    
    db.session.add(new_level)
    db.session.commit()

    return redirect(url_for('edit.add_level_done'))

@edit.route('/add/level/done')
@login_required
def add_level_done():
    flash('ユーザー登録を行いました。')

    return redirect(url_for('edit.show'))