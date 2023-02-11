from flask import Blueprint, render_template, request, \
    flash, url_for, redirect,session, g
from flask_login import login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

from sksk_app import db
from sksk_app.models.questions import User

class ManageUser:

    def register_user(name, email, password):
        regiestered_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        new_user = User(
            name = name,
            email = email,
            password = generate_password_hash(password, method='sha256'),
            registered_at = regiestered_at      
            )
        
        db.session.add(new_user)
        db.session.commit()




