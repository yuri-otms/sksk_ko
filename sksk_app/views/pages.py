from flask import Blueprint, redirect, url_for, render_template, session
from datetime import datetime
from sksk_app.models import Grade

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