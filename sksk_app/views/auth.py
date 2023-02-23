from flask import Blueprint, render_template, request, \
    flash, url_for, redirect,session
from flask_login import logout_user, login_required
from datetime import datetime

from sksk_app import db
from sksk_app.models import User, Score, Question
import sksk_app.utils.user as user_setting

auth = Blueprint('auth', __name__, url_prefix='/auth')

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

    user_setting.UserManager.register_user(name, email, password)

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
        user_setting.LoginManager.login(email, password)
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

@auth.route('/account')
@login_required
def account():
    user_id = session.get('user_id')

    user = db.session.get(User, user_id)

    # 今まで解いてきた問題数
    all_count = Score.query.filter(Score.user==user_id).count()
    correct_answers = Score.query.filter(Score.user==user_id).filter(Score.correct==1).count()
    # 正答率
    all_ratio = '{:.0%}'.format(correct_answers/all_count)
    grades_info = user_setting.ScoreManager.culculate_ratio_each_grade(user_id)

    return render_template('account.html', user=user, all_count=all_count,all_ratio=all_ratio, grades_info=grades_info)


@auth.errorhandler(404)
def non_existatnt_route(error):
    return redirect(url_for('auth.login'))


