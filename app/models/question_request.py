from database import db

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
   