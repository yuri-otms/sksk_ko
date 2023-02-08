from flask import Blueprint, render_template, request, flash, url_for, redirect
from sksk_ko import app
from datetime import datetime
from sksk_ko import db
from sksk_ko.models.questions import User
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)

@auth.route('/signup')
def signup():
    page_title = 'ユーザー登録'
    return render_template('auth/signup.html', page_title=page_title)

@auth.route('/signup', methods=['post'])
def signup_post():
    name = request.form['email']
    email = request.form['name']
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

    return redirect(url_for('auth.login'))

@auth.route('/login', methods=['GET','POST'])
def login():
    page_title = 'ログイン'
    return render_template('auth/login.html',page_title=page_title, )