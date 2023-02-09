

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

from sksk_ko import db

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

class E_Group(db.Model):
    __tablename__ = 'e_group'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    grade = db.Column(db.Integer, db.ForeignKey('grade.id'))
    e_group = db.Column(db.String(100))
    description = db.Column(db.String(100))

    def __init__(self, grade=None, e_group=None, description=None):
        self.grade = grade
        self.e_group = e_group
        self.description = description
    
    def __repr__(self):
        return '<Group id:{} grade:{} e_group:{} description:{}>'.format(self.id, self.grade, self.e_group, self.description)


class Element(db.Model):
    __tablename__ = 'element'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    e_group = db.Column(db.Integer, db.ForeignKey('e_group.id'))
    no = db.Column(db.Integer, unique=True)
    element = db.Column(db.String(40))
    description = db.Column(db.String(100))


    def __init__(self, e_group=None, no=None,element=None, description=None):
        self.e_group = e_group
        self.no = no
        self.element = element
        self.description = description
    
    def __repr__(self):
        return '<Element id:{} group:{} no:{} element:{} description:{}>'.format(self.id, self.grade, self.group, self.no,  self.element, self.description)

class Question(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    element = db.Column(db.Integer, db.ForeignKey('element.id'))
    japanese = db.Column(db.String(100))
    foreign_l = db.Column(db.String(100))
    style = db.Column(db.Integer, db.ForeignKey('style.id'))


    def __init__(self, element=None, japanese=None,foreign_l=None, style=None):
        self.element = element
        self.japanese = japanese
        self.foreign_l = foreign_l
        self.style = style
    
    def __repr__(self):
        return '<Element id:{} element:{} japanese:{} foreign:{} style:{}>'.format(self.id, self.element, self.japanese, self.foreign_l, self.style)


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
