from flask import request
from sqlalchemy import func
from datetime import datetime

from sksk_app import db
from sksk_app.models import Grade, E_Group, Element, Question, Word, Hint, Style, Record, Score

class RequestManager:

    def fetch_checked_question_infomation(questions_id, checked_conditions, messages):
        questions_raw = []
        for question_id in questions_id:
            question = Question.query.with_entities(Question.id, Grade.grade, Element.element, Question.japanese, Question.foreign_l).join(Element).join(E_Group).join(Grade).filter(Question.id==question_id).first()
            questions_raw.append(question)

        questions = []
        index = 0
        for question_raw in questions_raw:

            for checked_condition in checked_conditions:
                if question_raw.id == int(checked_condition):
                    checked = "確認済み"
                else:
                    checked = "再提出依頼"

            question = {
                "id": question_raw.id,
                "grade": question_raw.grade,
                "element": question_raw.element,
                "japanese": question_raw.japanese,
                "foreign_l": question_raw.foreign_l,
                "checked": checked,
                "message": messages[index]
            }
            questions.append(question)
            index += 1

        return questions