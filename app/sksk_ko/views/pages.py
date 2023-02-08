from flask import Blueprint, redirect, url_for, render_template
from sksk_ko.models.questions import Grade

pg = Blueprint('pg', __name__)


@pg.route('/')
def toppage():
    grades = Grade.query.order_by(Grade.id.asc()).all()
    return render_template("index.html", grades=grades)

@pg.route('/howto')
def howto():
    page_title = "使い方"
    return render_template("howto.html", page_title=page_title)

@pg.route('/about')
def about():
    page_title = "ABOUT"
    return render_template("about.html", page_title=page_title)