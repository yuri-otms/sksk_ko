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

@pg.route('/howto')
def howto():
    page_title = "使い方"
    return render_template("howto.html", page_title=page_title)

@pg.route('/about')
def about():
    page_title = "ABOUT"
    return render_template("about.html", page_title=page_title)

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


