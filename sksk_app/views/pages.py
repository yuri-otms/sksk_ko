from flask import Blueprint, redirect, url_for, render_template
from sksk_app.models import Grade

pg = Blueprint('pg', __name__)

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