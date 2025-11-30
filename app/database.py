from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from dotenv import load_dotenv
import os

db = SQLAlchemy()

def init_db(app: Flask):

    DB_USER = os.getenv("MYSQL_USER")
    DB_PASSWORD = os.getenv("MYSQL_PASSWORD")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_NAME = os.getenv("MYSQL_DATABASE")


    app.config["SQLALCHEMY_DATABASE_URI"] = (
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}?charset=utf8mb4"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)