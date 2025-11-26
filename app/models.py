from sqlalchemy import Column, Integer, String, Boolean
# from sksk_app.database import Base
from flask_login import UserMixin
from flask import current_app

from app import db

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

class Question_Request(db.Model):
    __tablename__ = 'question_request'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    client = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"))
    process = db.Column(db.Integer, db.ForeignKey('process.id', ondelete="CASCADE"))
    title = db.Column(db.String(500))
    detail = db.Column(db.Text)
    requested_at = db.Column(db.DateTime, nullable=False, default=False)
    checked_by = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"))
    finished_at = db.Column(db.DateTime)
    request_id = db.Column(db.Integer, default=0)
    read = db.Column(db.Boolean, nullable=False, default=False)
    requested_question = db.relationship("Requested_Question", backref='question_request_requested_question')

    def __init__(self, client=None, process=None, title=None, detail=None, requested_at=None, checked_by=None, finished_at=None,request_id=None, read=None):
        self.client = client
        self.process = process
        self.title = title
        self.detail = detail
        self.requested_at = requested_at
        self.checked_by = checked_by
        self.finished_at = finished_at
        self.request_id = request_id
        self.read = read
    
    def __repr__(self):
        return '<Question_Request id:{} client:{} pricess:{} title:{} detail:{} requested_at:{} checked_by:{} finished_at:{} request_id:{} read:{}'.format(self.id, self.client, self.process, self.title, self.detail, self.requested_at, self.checked_by, self.finished_at, self.request_id, self.read)
    
class Requested_Question(db.Model):
    __tablename__ = 'requested_question'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    request_id = db.Column(db.Integer, db.ForeignKey('question_request.id', ondelete="CASCADE"))
    question = db.Column(db.Integer, db.ForeignKey('question.id', ondelete="CASCADE"))

    def __init__(self, request_id=None, question=None):
        self.request_id = request_id
        self.question = question

    def __repr__(self):
        return '<Requested_Question id:{} request_id:{} question:{}>'.format(self.id, self.request_id, self.question)

class Privilege(db.Model):
    __tablename__ = 'privilege'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    privilege = db.Column(db.String(10))

    def __init__(self, privilege=True):
        self.privilege = privilege
    
    def __repr__(self):
        return '<Privilege id:{} privilege:{}>'.format(self.id, self.privilege)
    
class Process(db.Model):
    __tablename__ = 'process'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    process = db.Column(db.String(10))

    def __init__(self, process=True):
        self.process = process
    
    def __repr__(self):
        return '<Process id:{} process:{}>'.format(self.id, self.process)


class Score(db.Model):
    __tablename__ = 'score'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"))
    question = db.Column(db.Integer, db.ForeignKey('question.id', ondelete="CASCADE"))
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


class Grade(db.Model):
    __tablename__ = 'grade'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    grade = db.Column(db.String(30), unique=True)
    description = db.Column(db.String(100))
    position = db.Column(db.Integer, default=1)
    e_group = db.relationship("E_Group", backref='grade_e_group')

    def __init__(self, grade=None, description=None, position=None):
        self.grade = grade
        self.description = description
        self.position = position
    
    def __repr__(self):
        return '<Grade id:{} grade:{} description:{} posision:{}>'.format(self.id, self.grade, self.description, self.position)

class E_Group(db.Model):
    __tablename__ = 'e_group'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    grade = db.Column(db.Integer, db.ForeignKey('grade.id', ondelete="CASCADE"))
    e_group = db.Column(db.String(100))
    description = db.Column(db.String(100))
    position = db.Column(db.Integer, default=1)
    element = db.relationship("Element", backref='e_group_element')

    def __init__(self, grade=None, e_group=None, description=None, position=None):
        self.grade = grade
        self.e_group = e_group
        self.description = description
        self.position = position
    
    def __repr__(self):
        return '<E_Group id:{} grade:{} e_group:{} description:{} position:{}>'.format(self.id, self.grade, self.e_group, self.description, self.position)

class Element(db.Model):
    __tablename__ = 'element'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    e_group = db.Column(db.Integer, db.ForeignKey('e_group.id', ondelete="CASCADE"))
    element = db.Column(db.String(40))
    description = db.Column(db.String(100))
    position = db.Column(db.Integer, default=1)
    question = db.relationship("Question", backref='element_question')


    def __init__(self, e_group=None, element=None, description=None, position=None):
        self.e_group = e_group
        self.element = element
        self.description = description
        self.position = position
    
    def __repr__(self):
        return '<Element id:{} e_group:{} element:{} description:{} position:{}>'.format(self.id, self.e_group, self.element, self.description, self.position)
    
class Level(db.Model):
    __tablename__ = 'level'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    level = db.Column(db.Integer)

class Question(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    element = db.Column(db.Integer, db.ForeignKey('element.id', ondelete="CASCADE"))
    level = db.Column(db.Integer, db.ForeignKey('level.id', ondelete="CASCADE"))
    japanese = db.Column(db.String(100))
    foreign_l = db.Column(db.String(100))
    style = db.Column(db.Integer, db.ForeignKey('style.id', ondelete="CASCADE"))
    spoken = db.Column(db.Boolean, nullable=False, default=0)
    sida = db.Column(db.Boolean, nullable=False, default=0)
    will = db.Column(db.Boolean, nullable=False, default=0)
    position = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    process = db.Column(db.Integer, db.ForeignKey('process.id'))
    scores = db.relationship("Score", backref='question_score')
    hints = db.relationship("Hint", backref='question_hint')
    requested_question = db.relationship("Requested_Question", backref='question_requested_question')


    def __init__(self, element=None, level=None, japanese=None,foreign_l=None, style=None, spoken=None, sida=None, will=None, position=None, created_at=None, created_by=None, process=None):
        self.element = element
        self.level = level
        self.japanese = japanese
        self.foreign_l = foreign_l
        self.style = style
        self.spoken = spoken
        self.sida = sida
        self.will = will
        self.position = position
        self.created_at = created_at
        self.created_by =created_by
        self.process = process
    
    def __repr__(self):
        return '<Element id:{} element:{} level:{} japanese:{} foreign:{} style:{} spoken:{} sida:{} will:{} position:{} created_at:{} created_by:{} process:{}>'.format(self.id, self.element, self.level, self.japanese, self.foreign_l, self.style, self.spoken, self.sida, self.will, self.position, self.created_at, self.created_by, self.process)

class Record(db.Model):
    __tablename__  = 'record'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"))
    question = db.Column(db.Integer)
    process = db.Column(db.Integer, db.ForeignKey('process.id', ondelete="CASCADE"))
    message = db.Column(db.Text)
    executed_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, user=None, question=None, process=None, message=None, executed_at=None):
        self.user = user
        self.question = question
        self.process = process
        self.message = message
        self.executed_at = executed_at

    def __repr__(self):
        return '<Recoord id:{} user:{} question:{} process:{} message:{} executed_at:{}>'.format(self.id, self.user, self.question, self.process, self.message, self.executed_at)

class Word(db.Model):
    __tablename__ = 'word'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    japanese = db.Column(db.String(100))
    foreign_l = db.Column(db.String(100))
    hint = db.relationship("Hint", cascade="all,delete", backref='word_hint')

    def __init__(self, japanese=None, foreign_l=None):
        self.japanese = japanese
        self.foreign_l = foreign_l
    
    def __repr__(self):
        return '<Word id:{} japanese:{} foreign:{}>'.format(self.id, self.japanese, self.foreign_l)

class Hint(db.Model):
    __tablename__ = 'hint'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    question = db.Column(db.Integer, db.ForeignKey('question.id', ondelete="CASCADE"))
    word = db.Column(db.Integer, db.ForeignKey('word.id', ondelete="CASCADE"))


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
