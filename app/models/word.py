from database import db

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
