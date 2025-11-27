from database import db

 
class Process(db.Model):
    __tablename__ = 'process'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    process = db.Column(db.String(10))

    def __init__(self, process=True):
        self.process = process
    
    def __repr__(self):
        return '<Process id:{} process:{}>'.format(self.id, self.process)

