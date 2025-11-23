from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "Flask minimal app is running!"