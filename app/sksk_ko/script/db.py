from flask.cli import with_appcontext
from sksk_ko import app
from sksk_ko import db
from flask import Blueprint
from sksk_ko.models.questions import Grade

qtdb = Blueprint('qtdb', __name__)

# コマンド機能の作成
@qtdb.cli.command(name='create')
@with_appcontext
def create():
    with app.app_context():
        db.create_all()
        
# コマンド機能をcli commandsに追加
app.cli.add_command(create)