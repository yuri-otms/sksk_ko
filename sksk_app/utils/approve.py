from sksk_app import db
from sksk_app.models import Level, E_Group, Element, Question

class ReleaseManager:

    def change_level_settings(level_id):

        level = db.session.get(Level, level_id)

        if level.released:
            level.released = False

            db.session.merge(level)
            db.session.commit()
        else:
            level.released = True

            db.session.merge(level)
            db.session.commit()

    def change_e_group_settings(e_group_id):

        e_group = db.session.get(E_Group, e_group_id)

        if e_group.released:
            e_group.released = False

            db.session.merge(e_group)
            db.session.commit()
        else:
            e_group.released = True

            db.session.merge(e_group)
            db.session.commit()

    def change_element_settings(element_id):

        element = db.session.get(Element, element_id)

        if element.released:
            element.released = False

            db.session.merge(element)
            db.session.commit()
        else:
            element.released = True

            db.session.merge(element)
            db.session.commit()

    def change_question_settings(question_id):

        question = db.session.get(Question, question_id)

        if question.released:
            question.released = False

            db.session.merge(question)
            db.session.commit()
        else:
            question.released = True

            db.session.merge(question)
            db.session.commit()

    def release_questions(questions):

        for question_id in questions:
            question = db.session.get(Question, question_id)
            question.released = True
            db.session.merge(question)
        db.session.commit()

    def unrelease_questions(questions):

        for question_id in questions:
            question = db.session.get(Question, question_id)
            question.released = False
            db.session.merge(question)
        db.session.commit()

        
