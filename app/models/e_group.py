from database import db

class E_Group(db.Model):
    __tablename__ = 'e_group'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    grade = db.Column(db.Integer, db.ForeignKey('grade.id', ondelete="CASCADE"))
    e_group = db.Column(db.String(100))
    description = db.Column(db.String(100))
    position = db.Column(db.Integer, default=1)
    element = db.relationship("Element", backref='e_group_element')

    def __init__(self, grade=None, e_group=None, description=None, position=None):
        self.grade = grade
        self.e_group = e_group
        self.description = description
        self.position = position
    
    def __repr__(self):
        return '<E_Group id:{} grade:{} e_group:{} description:{} position:{}>'.format(self.id, self.grade, self.e_group, self.description, self.position)
