from database import db


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
