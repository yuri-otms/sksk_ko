from flask import Blueprint, render_template, request, \
    flash, url_for, redirect,session, Markup
from flask_login import logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from sqlalchemy import func

from app import db
from models.user import User
from models.score import Score
from models.question import Question
import app.utils.user as user_setting

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
    session.pop('edit', None)
    session.pop('check', None)
    session.pop('approve', None)
    session.pop('admin', None)

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




    return render_template('auth/account.html', user=user, all_count=all_count,all_ratio=all_ratio, grades_info=grades_info, incorrect_count=incorrect_count)

@auth.route('/edit/account')
@login_required
def edit_account():
    user_id = session.get('user_id')
    user = db.session.get(User, user_id)

    return render_template('auth/edit_account.html', user=user)

@auth.route('/edit/account/check', methods=['POST'])
@login_required
def edit_account_check():
    user_id = session.get('user_id')
    user = db.session.get(User, user_id)
    name = request.form['name']
    email = request.form['email']

    # emailに重複がないか調べる
    email_exist = User.query.filter(User.id==user_id).filter(User.email==email).first()
    if not email_exist:
        user = User.query.filter_by(email=email).first()
        if user:
            flash('メールアドレスが既に登録されています。')
            return redirect(url_for('auth.edit_account'))


    return render_template('auth/edit_account_check.html', user=user, name=name, email=email)

@auth.route('/edit/account/execute', methods=['POST'])
@login_required
def edit_account_execute():
    user_id = session.get('user_id')
    name = request.form['name']
    email = request.form['email']

    user_setting.UserManager.edit_user_name_email(user_id, name, email)

    session['user_name'] = name

    return redirect(url_for('auth.edit_account_done'))

@auth.route('/edit/account/done')
@login_required
def edit_account_done():
    flash('ユーザー情報を変更しました')
    return redirect(url_for('auth.account'))

@auth.route('/edit/password')
@login_required
def edit_password():
    user_id = session.get('user_id')
    user = db.session.get(User, user_id)

    return render_template('auth/edit_password.html', user=user)


@auth.route('/edit/password/execute', methods=['POST'])
@login_required
def edit_password_execute():
    user_id = session.get('user_id')
    user = db.session.get(User, user_id)
    
    current_password = request.form['current_password']
    new_password1 = request.form['new_password1']
    new_password2 = request.form['new_password2']

    
    if not check_password_hash(user.password, current_password):
        flash('現在のパスワードが異なります')
        return redirect(url_for('auth.edit_password'))
    
    if new_password1 !=new_password2 :
        flash('新しいパスワードが一致しません')
        return redirect(url_for('auth.edit_password'))
    
    user_setting.UserManager.edit_password(user_id, new_password1)
    
    return redirect(url_for('auth.edit_password_done'))

@auth.route('/edit/password/done')
@login_required
def edit_password_done():
    flash('パスワードを変更しました。')
    return redirect(url_for('auth.account'))

@auth.route('/delete/account')
@login_required
def delete_account():
    user_id = session.get('user_id')
    user = db.session.get(User, user_id)
    return render_template('auth/delete_account.html', user=user)

@auth.route('/delete/account/execute', methods=['POST'])
@login_required
def delete_account_execute():
    user_id = session.get('user_id')
    user_setting.UserManager.delete_user(user_id)
    return redirect(url_for('auth.delete_account_done'))

@auth.route('/delete/account/done')
@login_required
def delete_account_done():
    message = Markup('アカウントを削除しました。<br>ご利用ありがとうございました。')
    flash(message)
    logout_user()
    session.pop('user_id', None)
    session.pop('user', None)
    session.pop('edit', None)
    session.pop('check', None)
    session.pop('approve', None)
    session.pop('admin', None)
    return redirect(url_for('pg.toppage'))


@auth.errorhandler(404)
def non_existatnt_route(error):
    return redirect(url_for('auth.login'))


