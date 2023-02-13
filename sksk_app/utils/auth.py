from flask import Blueprint, render_template, request, \
    flash, url_for, redirect,session, g
from flask_login import login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

from sksk_app import db
from sksk_app.models import User, Process


class UserManager:

    def register_user(name, email, password):
        regiestered_at = datetime.now()

        new_user = User(
            name = name,
            email = email,
            password = generate_password_hash(password, method='sha256'),
            registered_at = regiestered_at      
            )
        
        db.session.add(new_user)
        db.session.commit()

    def register_user_priv(name, email, password, edit, check, approve, admin):
        regiestered_at = datetime.now()

        new_user = User(
            name = name,
            email = email,
            password = password,
            edit = edit,
            check = check,
            approve = approve,
            admin = admin,
            registered_at = regiestered_at      
            )
    
        db.session.add(new_user)
        db.session.commit()

    def delete_user(id):
        user = db.session.get(User, id)
        db.session.delete(user)
        db.session.commit()

    def edit_user(id, name, email, edit, check, approve, admin):

        user = db.session.get(User, id)

        user.name = name
        user.email = email
        user.edit = edit
        user.check = check
        user.approve = approve
        user.admin = admin

        db.session.merge(user)
        db.session.commit()

    def add_privilege(user, process):

        user = db.session.get(User, user)

        if process == 1:
            user.edit = True
        if process == 2:
            user.check = True
        if process == 3:
            user.approve = True
        if process == 4:
            user.admin = True

        db.session.merge(user)
        db.session.commit()
    
    def delete_privilege(user, process):

        user = db.session.get(User, user)

        if process == 1:
            user.edit = False
        if process == 2:
            user.check = False
        if process == 3:
            user.approve = False
        if process == 4:
            user.admin = False

        db.session.merge(user)
        db.session.commit()

    def register_process():

        processes = ['編集', '確認', '承認', '管理']
        for process in processes:
            process = Process(
                process = process
            )
            db.session.add(process)

        db.session.commit()



