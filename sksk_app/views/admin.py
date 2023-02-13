from flask import Blueprint, redirect, url_for, render_template, \
    request, flash
from sksk_app import db
from sksk_app.models import User, Process

from sksk_app.utils.auth import UserManager

admin = Blueprint('admin', __name__, url_prefix='/auth')

@admin.route('/')
def index():
    return render_template('admin/index.html')

@admin.route('/user')
def show_user():
    users = User.query.all()
    return render_template('admin/edit_user.html', users = users)

@admin.route('/add_privilege/', methods=['GET'])
def add_privilege():
    user_id = request.args.get('user_id')
    process_id = request.args.get('process_id')
    process = db.session.get(Process, process_id)
    user = db.session.get(User, user_id)
    return render_template('admin/add_privilege.html', process = process, user = user)

@admin.route('/privilege_added/', methods=['GET'])
def add_privilege_execute():
    user_id = request.args.get('user_id')
    process_id = int(request.args.get('process_id'))

    UserManager.add_privilege(user_id, process_id)

    return redirect(url_for('admin.add_privilege_done'))

@admin.route('/privilege_added_done')
def add_privilege_done():
    flash('権限が付与されました。')
    return redirect(url_for('admin.show_user'))

@admin.route('/delete_privilege/', methods=['GET'])
def delete_privilege():
    user_id = request.args.get('user_id')
    process_id = request.args.get('process_id')
    process = db.session.get(Process, process_id)
    user = db.session.get(User, user_id)
    return render_template('admin/delete_privilege.html', process = process, user = user)


@admin.route('/privilege_deleted/', methods=['GET'])
def delete_privilege_execute():
    user_id = request.args.get('user_id')
    process_id = int(request.args.get('process_id'))

    UserManager.delete_privilege(user_id, process_id)

    return redirect(url_for('admin.delete_privilege_done'))

@admin.route('/privilege_deleted_done')
def delete_privilege_done():
    flash('権限が削除されました。')
    return redirect(url_for('admin.show_user'))

