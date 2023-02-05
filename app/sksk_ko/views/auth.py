from flask import Blueprint, redirect, url_for, render_template, request, flash
from sksk_ko import app
from datetime import datetime

auth = Blueprint('auth', __name__)


@auth.route('/signup')
def signup():
    page_title = 'ユーザー登録'
    return render_template('auth/signup.html', page_title=page_title)
