from flask import Blueprint, redirect, url_for, render_template
from sksk_app.models.questions import Level

pg = Blueprint('pg', __name__)

@pg.route('/')
def toppage():
    level = Level.query.order_by(Level.id.asc()).first()
    return render_template("index.html", level = level)

@pg.route('/howto')
def howto():
    page_title = "使い方"
    return render_template("howto.html", page_title=page_title)

@pg.route('/about')
def about():
    page_title = "ABOUT"
    return render_template("about.html", page_title=page_title)