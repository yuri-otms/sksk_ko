from flask import Blueprint, render_template, request, \
    flash, url_for, redirect,session
from flask_login import logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from sqlalchemy import func

from sksk_app import db
from sksk_app.models import User, Score, Question
import sksk_app.utils.user as user_setting

auth = Blueprint('auth', __name__, url_prefix='/auth')


@auth.before_request
def load_logged_in_user():
    this_year = session.get('this_year')

    if not this_year:
       session['this_year'] = datetime.now().year

@auth.route('/signup')
def signup():
    page_title = 'ユーザー登録'
    return render_template('auth/signup.html', page_title=page_title)

@auth.route('/signup/check', methods=['post'])
def signup_check():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']

    user = User.query.filter_by(email=email).first()
    if user:
        flash('メールアドレスが既に登録されています。')
        return redirect(url_for('auth.signup'))
     
    return render_template('auth/signup_check.html', name=name, email=email, password=password)


# RPGデータ登録
@auth.route('/signup', methods=['post'])
def signup_post():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']

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
        question = int(request.form['question'])

        user_setting.LoginManager.login(email, password)

        if question:
            return redirect(url_for('question.check_login'))
        else:
            return redirect(url_for('pg.toppage'))

    if request.args.get('question'):
        question = int(request.args.get('question'))
    else:
        question = 0
    page_title = 'ログイン'
    return render_template('auth/login.html',page_title=page_title, question=question)


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
    if all_count:
        all_ratio = '{:.0%}'.format(correct_answers/all_count)
    else:
        all_ratio = '0%'
    grades_info = user_setting.ScoreManager.culculate_ratio_each_grade(user_id)


    # select question from score where correct = 0 and id in (select max(id) from score where user = 1 group by question);
    latest_answers = Score.query.with_entities(func.max(Score.id)).filter(Score.user==user_id).group_by(Score.question)
    incorrect_count = Score.query.filter(Score.correct==0).filter(Score.id.in_(latest_answers)).count()




    return render_template('account.html', user=user, all_count=all_count,all_ratio=all_ratio, grades_info=grades_info, incorrect_count=incorrect_count)


@auth.errorhandler(404)
def non_existatnt_route(error):
    return redirect(url_for('auth.login'))


