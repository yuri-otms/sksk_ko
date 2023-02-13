from flask import Blueprint, redirect, url_for, render_template, \
    request, flash, session
from flask_login import login_required
from sqlalchemy import not_
from sksk_app import db
from sksk_app.models import User, Process

from sksk_app.utils.auth import UserManager

admin = Blueprint('admin', __name__, url_prefix='/admin')

@admin.before_request
def load_logged_in_user():
    admin = session.get('admin')

    if not admin:
        flash('アクセスが許可されていません')
        return redirect(url_for('pg.toppage'))

@admin.route('/')
@login_required
def index():
    return render_template('admin/index.html')

@admin.route('/user')
@login_required
def show_user():
    users = User.query.all()
    return render_template('admin/users.html', users = users)

# 権限の付与
@admin.route('/add_privilege', methods=['GET'])
@login_required
def add_privilege():
    user_id = request.args.get('user_id')
    process_id = request.args.get('process_id')
    process = db.session.get(Process, process_id)
    user = db.session.get(User, user_id)
    return render_template('admin/add_privilege.html', process = process, user = user)

@admin.route('/privilege_added', methods=['GET'])
@login_required
def add_privilege_execute():
    user_id = request.args.get('user_id')
    process_id = int(request.args.get('process_id'))

    UserManager.add_privilege(user_id, process_id)

    return redirect(url_for('admin.add_privilege_done'))

@admin.route('/privilege_added_done')
@login_required
def add_privilege_done():
    flash('権限が付与されました。')
    return redirect(url_for('admin.show_user'))

# 権限の削除
@admin.route('/delete_privilege/', methods=['GET'])
@login_required
def delete_privilege():
    user_id = request.args.get('user_id')
    process_id = request.args.get('process_id')
    process = db.session.get(Process, process_id)
    user = db.session.get(User, user_id)
    return render_template('admin/delete_privilege.html', process = process, user = user)


@admin.route('/privilege_deleted/', methods=['GET'])
@login_required
def delete_privilege_execute():
    user_id = request.args.get('user_id')
    process_id = int(request.args.get('process_id'))

    UserManager.delete_privilege(user_id, process_id)

    return redirect(url_for('admin.delete_privilege_done'))

@admin.route('/privilege_deleted_done')
@login_required
def delete_privilege_done():
    flash('権限が削除されました。')
    return redirect(url_for('admin.show_user'))

# ユーザーの追加
@admin.route('/add_user', methods=['POST'])
@login_required
def add_user():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    edit = int(request.form['edit'])
    check = int(request.form['check'])
    approve = int(request.form['approve'])
    admin = int(request.form['admin'])

    user = User.query.filter_by(email=email).first()
    if user:
        flash('メールアドレスが既に登録されています。')
        return redirect(url_for('admin.show_user'))

    user = User(
        name = name,
        email = email,
        password = password,
        edit = edit,
        check = check,
        approve = approve,
        admin = admin
    )

    return render_template('admin/add_user.html', user = user)

@admin.route('/user_added', methods=['POST'])
@login_required
def add_user_execute():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    edit = int(request.form['edit'])
    check = int(request.form['check'])
    approve = int(request.form['approve'])
    admin = int(request.form['admin'])

    UserManager.register_user_priv(name, email, password, edit, check, approve, admin)

    return redirect(url_for('admin.add_user_done'))

@admin.route("/user_added_done")
@login_required
def add_user_done():

    flash('ユーザー登録を行いました。')

    return redirect(url_for('admin.show_user'))

# ユーザーの削除
@admin.route('/delete_user', methods=['GET'])
@login_required
def delete_user():
    user_id = request.args.get('id')

    user = User.query.filter_by(id=user_id).first()

    return render_template('admin/delete_user.html', user = user)

@admin.route('/user_deleted', methods=['GET'])
@login_required
def delete_user_execute():
    user_id = request.args.get('id')


    UserManager.delete_user(user_id)

    return redirect(url_for('admin.add_user_done'))

@admin.route("/user_deleted_done")
@login_required
def delete_user_done():

    flash('ユーザー登録を行いました。')

    return redirect(url_for('admin.show_user'))


# ユーザーの編集
@admin.route('/edit_user', methods=['GET'])
@login_required
def edit_user():
    user_id = request.args.get('id')
    user = db.session.get(User, user_id)

    return render_template('admin/edit_user.html', user = user)

@admin.route('/edit_user_check', methods=['POST'])
@login_required
def edit_user_check():
    id = request.form['id']
    name = request.form['name']
    email = request.form['email']
    edit = int(request.form['edit'])
    check = int(request.form['check'])
    approve = int(request.form['approve'])
    admin = int(request.form['admin'])

    user = User.query.filter(User.email==email).filter(not_(User.id==id)).first()
    if user:
        flash('メールアドレスが既に登録されています。')
        return redirect(url_for('admin.show_user'))

    user = User(
        name = name,
        email = email,
        edit = edit,
        check = check,
        approve = approve,
        admin = admin
    )

    return render_template('admin/edit_user_check.html',user_id=id, user = user)

@admin.route('/user_edited', methods=['POST'])
@login_required
def edit_user_execute():
    id = int(request.form["id"])
    name = request.form['name']
    email = request.form['email']
    edit = int(request.form['edit'])
    check = int(request.form['check'])
    approve = int(request.form['approve'])
    admin = int(request.form['admin'])

    UserManager.edit_user(id, name, email, edit, check, approve, admin)

    return redirect(url_for('admin.edit_user_done'))

@admin.route("/user_edited_done")
@login_required
def edit_user_done():

    flash('ユーザー編集を行いました。')

    return redirect(url_for('admin.show_user'))






