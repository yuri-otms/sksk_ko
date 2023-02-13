from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()

def create_app(test_config=None):

    app = Flask(__name__)

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_pyfile('test_config.py', silent=True)

    from sksk_app.models import db
    db.init_app(app) 

    from sksk_app.script.database import qtdb
    app.register_blueprint(qtdb)
    from sksk_app.views.pages import pg
    app.register_blueprint(pg)
    from sksk_app.views.auth import auth
    app.register_blueprint(auth)
    from sksk_app.views.edit import edit
    app.register_blueprint(edit)
    from sksk_app.views.admin import admin
    app.register_blueprint(admin)
    from sksk_app.views.questions import qt
    app.register_blueprint(qt)

    from sksk_app.models import User

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.login_message = u"ログインしてください。"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    return app







