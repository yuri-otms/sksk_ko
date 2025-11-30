from database import db
  
class Style(db.Model):
    __tablename__ = 'style'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    style = db.Column(db.String(10))

    def __init__(self, style=True):
        self.style = style
    
    def __repr__(self):
        return '<Style id:{} style:{}>'.format(self.id, self.style)
