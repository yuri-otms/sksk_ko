from sqlalchemy import func

from sksk_app import db
from sksk_app.models import Level, E_Group, Element, Question, Word, Hint

class LevelManager:
    def add_level(level, description):
        max_position = db.session.query(
            func.max(Level.position).label('level_max')).one()
        max = int(max_position.level_max)

        position = max + 1

        new_level = Level(
            level = level,
            description = description,
            position = position
        )
        
        db.session.add(new_level)
        db.session.commit()

class E_GroupManager:
    def add_e_group(level, e_group, description, position):
        if not position:
            max_position = E_Group.query.with_entities(func.max(E_Group.position).label('e_group_max')).filter(E_Group.level==level).one()
            max = int(max_position.e_group_max)
            position = max + 1

        new_e_group = E_Group(
            level = level,
            e_group = e_group,
            description = description,
            position = position
        )
        
        db.session.add(new_e_group)
        db.session.commit()