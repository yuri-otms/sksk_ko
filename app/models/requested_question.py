from database import db

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
