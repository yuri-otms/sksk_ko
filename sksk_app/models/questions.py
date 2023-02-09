from sksk_app import db
from flask_login import UserMixin

class Grade(db.Model):
    __tablename__ = 'grade'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    grade = db.Column(db.String(30), unique=True)
    description = db.Column(db.String(100))


    def __init__(self, grade=None, description=None):
        self.grade = grade
        self.description = description
    
    def __repr__(self):
        return '<Grade id:{} grade:{} description:{}>'.format(self.id, self.grade, self.description)

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    target_grade = db.Column(db.Integer, db.ForeignKey('grade.id'), nullable=False, default=1)
    edit = db.Column(db.Integer, nullable=False,default=0)
    check = db.Column(db.Integer, nullable=False,default=0)
    approve = db.Column(db.Integer, nullable=False,default=0)
    admin = db.Column(db.Integer, nullable=False,default=0)
    registered_at = db.Column(db.DateTime, nullable=False)


    def __init__(self, name=None, email=None, password=None, target_grade=None, edit=None, check=None, approve=None, admin=None, registered_at=None):
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
        return '<User id:{} name:{} password:{}>'.format(self.id, self.name, self.email, self.password, self.target_grade, self.edit, self.check, self.approve, self.admin, self.registered_at)
