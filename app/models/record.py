from database import db

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
