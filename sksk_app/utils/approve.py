from flask import session
from datetime import datetime

from sksk_app import db
from sksk_app.models import Grade, E_Group, Element, Question
import sksk_app.utils.edit as editor

class ReleaseManager:

    def change_grade_settings(grade_id):

        grade = db.session.get(Grade, grade_id)

        if grade.released:
            grade.released = False

            db.session.merge(grade)
            db.session.commit()
        else:
            grade.released = True

            db.session.merge(grade)
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

    def change_question_settings(user, question_id):

        question = db.session.get(Question, question_id)
        executed_at = datetime.now()
        message= 'なし'

        if question.released:
            question.released = False

            db.session.merge(question)
            db.session.commit()

            editor.QuestionManager.record_process(user, question_id, 3, 0, message, executed_at)

        else:
            question.released = True

            db.session.merge(question)
            db.session.commit()

            editor.QuestionManager.record_process(user, question_id, 3, 1, message, executed_at)

        

    def release_questions(user, questions):
        executed_at = datetime.now()
        message= 'なし'


        for question_id in questions:
            question = db.session.get(Question, question_id)
            question.released = True
            db.session.merge(question)
            db.session.commit()

            editor.QuestionManager.record_process(user, question_id, 3, 1, message, executed_at)


    def unrelease_questions(user, questions):
        executed_at = datetime.now()
        message= 'なし'


        for question_id in questions:
            question = db.session.get(Question, question_id)
            question.released = False
            db.session.merge(question)
            db.session.commit()

            editor.QuestionManager.record_process(user, question_id, 3, 0, message, executed_at)

        
