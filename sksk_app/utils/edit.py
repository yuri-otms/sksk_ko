from sqlalchemy import func

from sksk_app import db
from sksk_app.models import Level, E_Group, Element, Question, Word, Hint

class LevelManager:
    def add_level(level, description, position):
        if not position:
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
            e_group_exist = E_Group.query.filter(E_Group.level==level).first()
            if e_group_exist:
                max_position = E_Group.query.with_entities(func.max(E_Group.position).label('e_group_max')).filter(E_Group.level==level).one()
                max = int(max_position.e_group_max)
                position = max + 1
            else:
                position = 1

        new_e_group = E_Group(
            level = level,
            e_group = e_group,
            description = description,
            position = position
        )

        db.session.add(new_e_group)
        db.session.commit()

class ElementManager:
    def add_element(e_group, element, description, position):
        if not position:
            element_exist = Element.query.filter(Element.e_group==e_group).first()
            if element_exist:
                max_position = Element.query.with_entities(func.max(Element.position).label('element_max')).filter(Element.e_group==e_group).one()
                max = int(max_position.element_max)
                position = max + 1
            else:
                position = 1

        new_element = Element(
            e_group = e_group,
            element = element,
            description = description,
            position = position
        )

        db.session.add(new_element)
        db.session.commit()

