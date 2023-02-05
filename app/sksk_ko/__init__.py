from flask import Flask

app = Flask(__name__)


from sksk_ko.views.pages import pg
app.register_blueprint(pg)

from sksk_ko.views.auth import auth
app.register_blueprint(auth)

from sksk_ko.views.questions import qt
app.register_blueprint(qt)





