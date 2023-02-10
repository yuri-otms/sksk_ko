# from flask.cli import with_appcontext
from flask import current_app, Flask
from flask import Blueprint

from sksk_app import db

app = Flask(__name__)

qtdb = Blueprint('cli', __name__)

# コマンド機能の作成
@qtdb.cli.command('create')
def create():
    db.create_all()
    print("Create All Tables ")

app.cli.add_command(create)