from sksk_app import db
from sksk_app.models import Level


class QuestionManager:
    def delete_testing_levels():

        Level.query.filter(Level.id.between(10, 200)).delete()
        db.session.commit()
    
    def insert_level(level, description, position):

        new_level = Level(
            level = level,
            description = description,
            position = position
        )
        
        db.session.add(new_level)
        db.session.commit()