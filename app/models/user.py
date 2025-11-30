from flask_login import UserMixin
from database import db


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    target_grade = db.Column(db.Integer, db.ForeignKey('grade.id'), nullable=False, default=1)
    edit = db.Column(db.Boolean, nullable=False, default=False)
    check = db.Column(db.Boolean, nullable=False, default=False)
    approve = db.Column(db.Boolean, nullable=False, default=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    registered_at = db.Column(db.DateTime, nullable=False, default=False)
    score = db.relationship("Score", backref='user_score')


    def __init__(self, name=None, email=None, password=None,
        target_grade=None, edit=None, check=None, approve=None,
        admin=None, registered_at=None):
        self.name = name
        self.email = email
        self.password = password
        self.target_grade = target_grade
        self.edit = edit
        self.check = check
        self.approve = approve
        self.admin = admin
        self.registered_at = registered_at
    
    def __repr__(self):
        return '<User id:{} name:{} email:{} password:{} target_grade:{} edit:{} check:{} approve:{} admin:{} registered_at:{}>'.format(self.id, self.name, self.email, self.password, self.target_grade, self.edit, self.check, self.approve, self.admin, self.registered_at)
