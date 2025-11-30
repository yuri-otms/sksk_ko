from database import db

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
