from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():

    app = Flask(__name__)
    app.config.from_object('sksk_app.config')

    db.init_app(app)    

    # from sksk_app.script.db import qtdb
    from sksk_app.views.pages import pg
    from sksk_app.views.auth import auth
    from sksk_app.views.questions import qt
    # app.register_blueprint(qtdb)
    app.register_blueprint(pg)
    app.register_blueprint(auth)
    app.register_blueprint(qt)

    return app







