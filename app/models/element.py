from database import db


class Element(db.Model):
    __tablename__ = 'element'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    e_group = db.Column(db.Integer, db.ForeignKey('e_group.id', ondelete="CASCADE"))
    element = db.Column(db.String(40))
    description = db.Column(db.String(100))
    position = db.Column(db.Integer, default=1)
    question = db.relationship("Question", backref='element_question')


    def __init__(self, e_group=None, element=None, description=None, position=None):
        self.e_group = e_group
        self.element = element
        self.description = description
        self.position = position
    
    def __repr__(self):
        return '<Element id:{} e_group:{} element:{} description:{} position:{}>'.format(self.id, self.e_group, self.element, self.description, self.position)
 