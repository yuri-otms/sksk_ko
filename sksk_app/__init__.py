from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


db = SQLAlchemy()

def create_app(database_uri=None):

    app = Flask(__name__)
    app.config.from_object('sksk_app.config')

    if database_uri:
        app.config["SQLALCHEMY_DATABASE_URI"] = database_uri

    db.init_app(app) 

    from sksk_app.script.database import qtdb
    from sksk_app.views.pages import pg
    from sksk_app.views.auth import auth
    from sksk_app.views.edit import edit
    from sksk_app.views.questions import qt
    app.register_blueprint(qtdb)
    app.register_blueprint(pg)
    app.register_blueprint(auth)
    app.register_blueprint(edit)
    app.register_blueprint(qt)

    from sksk_app.models.questions import User

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.login_message = u"ログインしてください。"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    return app







