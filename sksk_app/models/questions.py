from sksk_app import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    target_level = db.Column(db.Integer, db.ForeignKey('level.id'), nullable=False, default=1)
    edit = db.Column(db.Boolean, nullable=False,default=0)
    check = db.Column(db.Boolean, nullable=False,default=0)
    approve = db.Column(db.Boolean, nullable=False,default=0)
    admin = db.Column(db.Boolean, nullable=False,default=0)
    registered_at = db.Column(db.DateTime, nullable=False)


    def __init__(self, name=None, email=None, password=None, target_level=None, edit=None, check=None, approve=None, admin=None, registered_at=None):
        self.name = name
        self.email = email
        self.password = password
        self.target_level = target_level
        self.edit = edit
        self.check = check
        self.approve = approve
        self.admin = admin
        self.registered_at = registered_at
    
    def __repr__(self):
        return '<User id:{} name:{} password:{}>'.format(self.id, self.name, self.email, self.password, self.target_level, self.edit, self.check, self.approve, self.admin, self.registered_at)


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


class Level(db.Model):
    __tablename__ = 'level'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    level = db.Column(db.String(30), unique=True)
    description = db.Column(db.String(100))
    released = db.Column(db.Boolean, nullable=False,default=0)


    def __init__(self, level=None, description=None, released=None):
        self.level = level
        self.description = description
        self.released = released
    
    def __repr__(self):
        return '<level id:{} level:{} description:{} released:{}>'.format(self.id, self.level, self.description, self.released)

class E_Group(db.Model):
    __tablename__ = 'e_group'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    level = db.Column(db.Integer, db.ForeignKey('level.id'))
    e_group = db.Column(db.String(100))
    description = db.Column(db.String(100))
    released = db.Column(db.Boolean, nullable=False,default=0)

    def __init__(self, level=None, e_group=None, description=None, released=None):
        self.level = level
        self.e_group = e_group
        self.description = description
        self.released = released
    
    def __repr__(self):
        return '<Group id:{} level:{} e_group:{} description:{} released:{}>'.format(self.id, self.level, self.e_group, self.description, self.released)

class Element(db.Model):
    __tablename__ = 'element'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    e_group = db.Column(db.Integer, db.ForeignKey('e_group.id'))
    no = db.Column(db.Integer, unique=True)
    element = db.Column(db.String(40))
    description = db.Column(db.String(100))
    released = db.Column(db.Boolean, nullable=False,default=0)


    def __init__(self, e_group=None, no=None,element=None, description=None, released=None):
        self.e_group = e_group
        self.no = no
        self.element = element
        self.description = description
        self.released = released
    
    def __repr__(self):
        return '<Element id:{} group:{} no:{} element:{} description:{} released:{}>'.format(self.id, self.level, self.group, self.no,  self.element, self.description, self.released)

class Question(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    element = db.Column(db.Integer, db.ForeignKey('element.id'))
    japanese = db.Column(db.String(100))
    foreign_l = db.Column(db.String(100))
    style = db.Column(db.Integer, db.ForeignKey('style.id'))
    released = db.Column(db.Boolean, nullable=False,default=0)


    def __init__(self, element=None, japanese=None,foreign_l=None, style=None, released=None):
        self.element = element
        self.japanese = japanese
        self.foreign_l = foreign_l
        self.style = style
        self.released = released
    
    def __repr__(self):
        return '<Element id:{} element:{} japanese:{} foreign:{} style:{} released:{}>'.format(self.id, self.element, self.japanese, self.foreign_l, self.style, self.released)


class Word(db.Model):
    __tablename__ = 'word'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    japanese = db.Column(db.String(100))
    foreign_l = db.Column(db.String(100))

    def __init__(self, japanese=None, foreign_l=None):
        self.japanese = japanese
        self.foreign_l = foreign_l
    
    def __repr__(self):
        return '<Word id:{} japanese:{} foreign:{}>'.format(self.id, self.japanese, self.foreign_l)

class Hint(db.Model):
    __tablename__ = 'hint'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    question = db.Column(db.Integer, db.ForeignKey('question.id'))
    word = db.Column(db.Integer, db.ForeignKey('word.id'))


    def __init__(self, question = None, word=None):
        self.question = question
        self.word = word
    
    def __repr__(self):
        return '<Hint id:{} question:{} word:{}>'.format(self.id, self.question, self.word)

class Style(db.Model):
    __tablename__ = 'style'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    style = db.Column(db.String(10))

    def __init__(self, style=True):
        self.style = style
    
    def __repr__(self):
        return '<Style id:{} style:{}>'.format(self.id, self.style)
