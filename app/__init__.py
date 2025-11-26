from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

import config as config

db = SQLAlchemy()

def create_app(test_config=None):
    app = Flask(__name__)

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_pyfile('test_config.py', silent=True)
    
    app.config['SECRET_KEY'] = config.SECRET_KEY

    from models import db
    db.init_app(app) 

    from script.database import qtdb
    app.register_blueprint(qtdb)
    from app.views.pages import pg
    app.register_blueprint(pg)
    from app.views.auth import auth
    app.register_blueprint(auth)
    from app.views.edit import edit
    app.register_blueprint(edit)
    from app.views.approve import approve
    app.register_blueprint(approve)
    from app.views.admin import admin
    app.register_blueprint(admin)
    from app.views.question import question
    app.register_blueprint(question)
    from app.views.request import req
    app.register_blueprint(req)

    from app.models import User

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.login_message = u"ログインしてください。"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    return app









if __name__ == '__main__':
    create_app().run(debug=True, use_reloader=True, use_debugger=True)