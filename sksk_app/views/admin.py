from datetime import datetime
from flask import Blueprint, redirect, url_for, render_template, \
    request, flash, session
from flask_login import login_required
from sqlalchemy import not_, or_
from sksk_app import db
from sksk_app.models import User, Process,Record

import sksk_app.utils.user as user_setting

admin = Blueprint('admin', __name__, url_prefix='/admin')

@admin.before_request
def load_logged_in_user():
    admin = session.get('admin')
    this_year = session.get('this_year')

    if not this_year:
       session['this_year'] = datetime.now().year

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

    user_setting.UserManager.add_privilege(user_id, process_id)

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

    user_setting.UserManager.delete_privilege(user_id, process_id)

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

    user_setting.UserManager.register_user_priv(name, email, password, edit, check, approve, admin)

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
    user_id = int(request.args.get('id'))

    if user_id == session.get('user_id'):
        flash('管理ユーザーは自身のアカウントを削除できません。')
        return redirect(url_for('admin.show_user'))


    user = User.query.filter_by(id=user_id).first()

    return render_template('admin/delete_user.html', user = user)

@admin.route('/user_deleted', methods=['POST'])
@login_required
def delete_user_execute():
    user_id = int(request.form['id'])

    if user_id == session.get('user_id'):
        flash('管理ユーザーは自身のアカウントを削除できません。')
        return redirect(url_for('admin.show_user'))

    user_setting.UserManager.delete_user(user_id)

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

    user_setting.UserManager.edit_user(id, name, email, edit, check, approve, admin)

    return redirect(url_for('admin.edit_user_done'))

@admin.route("/user_edited_done")
@login_required
def edit_user_done():

    flash('ユーザー編集を行いました。')

    return redirect(url_for('admin.show_user'))


@admin.route('/records')
@login_required
def show_records():

    # ユーザーidを取得、変更履歴
    if request.args.get('u'):
        if request.args.get('u') == '0':
            records_raw = Record.query.all()
            user_id = 0
        else:
            user_id = int(request.args.get('u'))
            records_raw = Record.query.filter(Record.user==user_id)
    else:
        records_raw = Record.query.all()
        user_id = 0

    # 変更履歴の取得
    records = []
    for record_raw in records_raw:
        process = db.session.get(Process, record_raw.process).process

        record = {
            "id":record_raw.id,
            "user":record_raw.user,
            "question":record_raw.question,
            "process_id":record_raw.process,
            "process":process,
            "message":record_raw.message,
            "executed_at":record_raw.executed_at
        }
        records.append(record)

    # 有効なユーザーの表示(何かしら権限のあるユーザー)
    users_raw = User.query.filter(or_(User.edit==1,User.check==1, User.approve==1, User.admin==1))
    users = []
    number = 1
    user = {"number":0, "id":0, "name":'全体'}
    for user_raw in users_raw:
        if user_raw.name != None:
            user_added = {
                "number":number,
                "id":user_raw.id,
                "name":user_raw.name
            }
            users.append(user_added)
            if user_added['id'] == user_id:
                user.update(user_added)
            number += 1

    # 全体の表示用情報
    all = {
        "number":0,
        "id":0,
        "name":'全体'
    }
    users.insert(0, all)




    return render_template('admin/show_records.html', records=records, users=users, user=user)

@admin.route('/edit/password')
@login_required
def edit_password():
    user_id = request.args.get('u')
    user = db.session.get(User, user_id)

    return render_template('admin/edit_password.html', user=user)

@admin.route('/edit/password_check', methods=['POST'])
@login_required
def edit_password_check():
    user_id = request.form['user_id']
    password = request.form['password']
    user = db.session.get(User, user_id)

    return render_template('admin/edit_password_check.html', user=user, password=password)


@admin.route('/edit/password_execute', methods=['POST'])
@login_required
def edit_password_execute():
    user_id = request.form['user_id']
    password = request.form['password']

    user_setting.UserManager.edit_password(user_id, password)

    return redirect(url_for('admin.edit_password_done'))

@admin.route('/edit/password_done')
@login_required
def edit_password_done():
    flash('パスワードを変更しました')

    return redirect(url_for('admin.show_user'))











