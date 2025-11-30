from database import db

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
