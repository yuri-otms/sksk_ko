from database import db

class Privilege(db.Model):
    __tablename__ = 'privilege'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    privilege = db.Column(db.String(10))

    def __init__(self, privilege=True):
        self.privilege = privilege
    
    def __repr__(self):
        return '<Privilege id:{} privilege:{}>'.format(self.id, self.privilege)
    