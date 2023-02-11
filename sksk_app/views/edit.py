from flask import Blueprint, redirect, url_for, render_template, request, \
    flash
from sqlalchemy import func

from sksk_app import db
from sksk_app.models.questions import Level

edit = Blueprint('edit', __name__, url_prefix='/edit')


@edit.route('/index')
def index():
    return render_template('edit/index.html')

@edit.route('/show')
def show():
    levels = db.session.query(Level).all()
    return render_template('edit/show.html', levels = levels)

@edit.route('/add/level', methods=['POST'])
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
def add_level_done():
    flash('ユーザー登録を行いました。')

    return redirect(url_for('edit.show'))