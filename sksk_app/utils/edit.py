from flask import request
from sqlalchemy import func

from sksk_app import db
from sksk_app.models import Level, E_Group, Element, Question, Word, Hint, Style

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

class StyleManager:
    def add_style(style):
        new_style = Style(
            style = style
        )

        db.session.add(new_style)
        db.session.commit()

class QuestionManager:
    def add_question(element, japanese, foreign_l, style, position):

        if not position:
            question_exist = Question.query.filter(Question.element==element).first()
            if question_exist:
                max_position = Question.query.with_entities(func.max(Question.position).label('question_max')).filter(Question.element==element).one()
                max = int(max_position.question_max)
                position = max + 1
            else:
                position = 1
        
        new_question = Question(
            element = element,
            japanese = japanese,
            foreign_l = foreign_l,
            style = style,
            position = position
        )

        db.session.add(new_question)
        db.session.commit()

class EditManager:
    
    def fetchLevel():
        if request.args.get('l'):
            level_id = request.args.get('l')
        else:
            level= Level.query.with_entities(func.min(Level.id).label('level_min')).first()
            level_id = level.level_min
        return level_id

    def fetchE_Group(level_id):
        if request.args.get('g'):
            e_group_id = request.args.get('g')
        else:
            e_group = E_Group.query.filter(E_Group.level == level_id).first()
            if e_group:
                e_group = E_Group.query.with_entities(E_Group.level, func.min(E_Group.id).label('e_group_min')).filter(E_Group.level==level_id).group_by(E_Group.level).one()
                e_group_id = e_group.e_group_min
            else:
                e_group_id = None
        return e_group_id
    
    def fetchElement(e_group_id):
        if request.args.get('e'):
            element_id = request.args.get('e')
        else:
            element = Element.query.filter(Element.e_group==e_group_id).first()
            if element:
                element = Element.query.with_entities(Element.e_group, func.min(Element.id).label('element_min')).filter(Element.e_group==e_group_id).group_by(Element.e_group).one()
                element_id = element.element_min
            else:
                element_id = None
        return element_id

    def addE_GroupName(level_id):
        e_groups_raw = db.session.query(E_Group).filter(E_Group.level==level_id)
        e_groups = []
        for e_group in e_groups_raw:
            level_name = db.session.get(Level, e_group.level)
            e_group_added = {
                "id":e_group.id,
                "level":e_group.level,
                "level_name":level_name.level,
                "e_group":e_group.e_group,
                "description":e_group.description,
                "position":e_group.position,
                "released":e_group.released
            }
            e_groups.append(e_group_added)

        return e_groups

