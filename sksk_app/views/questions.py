from flask import Blueprint, redirect, url_for, render_template

qt = Blueprint('qt', __name__, url_prefix='/question')


@qt.route('/select_grade')
def select_grade():
    pass