from flask import Blueprint, render_template, request, flash, url_for, redirect
from datetime import datetime
from sksk_app import db
from sksk_app.models.questions import User
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)

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
    regiestered_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    user = User.query.filter_by(email=email).first()

    if user:
        flash('メールアドレスが既に登録されています。')
        return redirect(url_for('auth.signup'))

    new_user = User(
        name = name,
        email = email,
        password = generate_password_hash(password, method='sha256'),
        registered_at = regiestered_at      
        )
    
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.signup_done'))

# RPG画面表示
@auth.route("/signup_done")
def signup_done():

    flash('ユーザー登録を行いました。')

    return redirect(url_for('auth.login'))


@auth.route('/login', methods=['GET','POST'])
def login():
    page_title = 'ログイン'
    return render_template('auth/login.html',page_title=page_title, )