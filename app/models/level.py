from database import db

class Level(db.Model):
    __tablename__ = 'level'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    level = db.Column(db.Integer)
