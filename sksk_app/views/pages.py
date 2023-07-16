from flask import Blueprint, redirect, url_for, render_template, session, request, flash
from datetime import datetime

from sksk_app.models import Grade
import sksk_app.utils.api as api

pg = Blueprint('pg', __name__)

@pg.before_request
def load_logged_in_user():
    this_year = session.get('this_year')

    if not this_year:
       session['this_year'] = datetime.now().year

@pg.route('/')
def toppage():
    return render_template("index.html")

@pg.route('/about')
def about():
    page_title = '「サクッと作文」について'
    return render_template('about.html', page_title=page_title)


@pg.route('/terms_of_service')
def terms_of_service():
    page_title = '利用規約'
    return render_template('terms_of_service.html', page_title=page_title)

@pg.route('/privacy_policy')
def privacy_policy():
    page_title = 'プライバシーポリシー'
    return render_template('privacy_policy.html', page_title=page_title)

@pg.route('/contact')
def contact():
    page_title = "お問い合わせ"
    return render_template('contact.html', page_title=page_title)

@pg.route('/contact/confirm', methods=['POST'])
def contact_confirm():
    name = request.form['name']
    email = request.form['email']
    title = request.form['title']
    message = request.form['message']
    
    page_title = "お問い合わせ"
    return render_template('contact_confirm.html', page_title=page_title, name=name, email=email, title=title, message=message)

@pg.route('/contact/execute', methods=['POST'])
def contact_execute():
    name = request.form['name']
    email = request.form['email']
    title = request.form['title']
    message = request.form['message']

    message_body = ' 名前: {}\n email: {}\n 件名: {}\n 本文: {}\n\n sksk-appお問い合わせフォームより送信されました。'.format(name, email, title, message)

    sender = 'skskapp.info@gmail.com'
    to = 'lstliauou@gmail.com'
    subject = 'sksk-app問い合わせフォームより'

    api.GoogleCloud.send_email(sender, to, subject, message_body)

    return redirect(url_for('pg.contact_done'))

@pg.route('/contact/done')
def contact_done():
    flash('お問い合わせ内容を送信しました。')

    return redirect(url_for('pg.toppage'))


@pg.route('/howto')
def howto():
    page_title = '使い方'
    return render_template('howto/index.html', page_title=page_title)

@pg.route('/howto/start_without_login')
def start_without_login():
    page_title = 'ログインしないで問題を解く'
    return render_template('howto/start_without_login.html', page_title=page_title)

@pg.route('/howto/signup')
def signup():
    page_title = 'ユーザー登録をする'
    return render_template('howto/signup.html', page_title=page_title)

@pg.route('/demo')
def demo():
    page_title = 'デモ版の注意点'
    return render_template('demo.html', page_title=page_title)