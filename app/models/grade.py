from database import db


class Grade(db.Model):
    __tablename__ = 'grade'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    grade = db.Column(db.String(30), unique=True)
    description = db.Column(db.String(100))
    position = db.Column(db.Integer, default=1)
    e_group = db.relationship("E_Group", backref='grade_e_group')

    def __init__(self, grade=None, description=None, position=None):
        self.grade = grade
        self.description = description
        self.position = position
    
    def __repr__(self):
        return '<Grade id:{} grade:{} description:{} posision:{}>'.format(self.id, self.grade, self.description, self.position)
