from flask import Blueprint, render_template, request, \
    flash, url_for, redirect,session
from flask_login import login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

from sksk_app.models import db, User
from sksk_app.utils.auth import UserManager

auth = Blueprint('auth', __name__, url_prefix='/auth')

# @auth.before_app_request
# def load_logged_in_user():
#     user_id = session.get('user_id')

#     if user_id is None:
#         g.user = None
#     else:
#         user = db.session.get(User, user_id)
#         user_list = {
#             'email':user.email,
#             'name':user.name,
#             'password':user.password
#         }
#         g.user = user_list

@auth.route('/signup')
def signup():
    page_title = 'ユーザー登録'
    return render_template('auth/signup.html', page_title=page_title)

# RPGデータ登録
@auth.route('/signup', methods=['post'])
def signup_post():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']

    user = User.query.filter_by(email=email).first()
    if user:
        flash('メールアドレスが既に登録されています。')
        return redirect(url_for('auth.signup'))

    UserManager.register_user(name, email, password)

    return redirect(url_for('auth.signup_done'))

# RPG画面表示
@auth.route("/signup_done")
def signup_done():

    flash('ユーザー登録を行いました。')

    return redirect(url_for('auth.login'))


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        
        if not user or not check_password_hash(user.password, password):
            flash('パスワードが異なります')
            return redirect(url_for('auth.login'))

        flash('ログインしました')
        login_user(user)
        session['user_id'] = user.id
        session['user_name'] = user.name
        session['edit'] = user.edit
        session['admin'] = user.admin
        return redirect(url_for('pg.toppage'))

    page_title = 'ログイン'
    return render_template('auth/login.html',page_title=page_title)


@auth.route('/logout')
def logout():
    logout_user()
    session.pop('user_id', None)
    session.pop('user', None)

    flash('ログアウトしました')
    return redirect(url_for('pg.toppage'))