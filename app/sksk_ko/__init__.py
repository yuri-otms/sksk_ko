from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('sksk_ko.config')

db = SQLAlchemy(app)


# Blueprint設定
from sksk_ko.script.db import qtdb
app.register_blueprint(qtdb)

from sksk_ko.views.pages import pg
app.register_blueprint(pg)

from sksk_ko.views.auth import auth
app.register_blueprint(auth)

from sksk_ko.views.questions import qt
app.register_blueprint(qt)
# Blueprint設定　終了





