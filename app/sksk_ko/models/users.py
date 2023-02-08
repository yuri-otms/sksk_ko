from sksk_ko import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(1000), unique=True)
    name = db.Column(db.String(100))
    password = db.Column(db.String(100))
    target_grade = db.Column(db.Integer, db.ForeignKey('grade.id'), nullable=False, default=1)
    admin = db.Column(db.Integer, nullable=False,default=0)
    registered_at = db.Column(db.DateTime, nullable=False)


    def __init__(self, email=None,name=None, password=None, target_grade=None,admin=None, registered_at=None):
        self.email = email
        self.name = name
        self.password = password
        self.target_grade = target_grade
        self.admin = admin
        self.registered_at = registered_at
    
    def __repr__(self):
        return '<User id:{} name:{} password:{}>'.format(self.id, self.email, self.name,self.password, self.target_grade, self.admin, self.registered_at)


class Score(db.Model):
    __tablename__ = 'score'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user = db.Column(db.Integer, db.ForeignKey('user.id'))
    question = db.Column(db.Integer, db.ForeignKey('question.id'))
    correct = db.Column(db.Boolean, nullable=False)
    review = db.Column(db.Boolean, nullable=False)
    answered_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, user=None, question=None, correct=None, review=None, answered_at=None):
        self.user = user
        self.question = question
        self.correct = correct
        self.review = review
        self.answered_at = answered_at
    
    def __repr__(self):
        return '<Score id:{} user:{} question:{} correct:{} answered_at:{}>'.format(self.id, self.user, self.question, self.correct, self.review, self.answered_at)