from flask import request
from sqlalchemy import func
from datetime import datetime

from sksk_app import db
from sksk_app.models import Grade, E_Group, Element, Question, Word, Hint, Style, Record, Score, Requested_Question, Question_Request

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
                    break
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
    
    def fetch_questions_with_check_message(request_id):

        questions_raw = Question.query.with_entities(Question.id, Grade.grade, Element.element, Question.japanese, Question.foreign_l).join(Element).join(E_Group).join(Grade).join(Requested_Question).filter(Requested_Question.request_id==request_id)

        questions = []
        for question_raw in questions_raw:
            record = Record.query.filter(Record.question==question_raw.id).order_by(Record.id.desc()).first()
            if record.process == 5:
                process_name = '確認済み'
            elif record.process == 6:
                process_name = '確認却下'
            else:
                process_name = ''

            question = {
                "id": question_raw.id,
                "grade": question_raw.grade,
                "element": question_raw.element,
                "japanese": question_raw.japanese,
                "foreign_l": question_raw.foreign_l,
                "checked": process_name,
                "message": record.message
            }
            questions.append(question)

        return questions

    def add_request(questions_requested, title, detail, user_id):
        now = datetime.now()

        new_request = Question_Request(
            client = user_id,
            process = 4,
            title = title,
            detail = detail,
            requested_at = now
        )
        db.session.add(new_request)
        db.session.commit()

        request_id = db.session.query(
                    func.max(Question_Request.id).label('latest')).one()

        for question_requested in questions_requested:
            new_requested_question = Requested_Question(
                request_id = request_id.latest,
                question = question_requested
            )
            db.session.add(new_requested_question)
            db.session.commit()

            question = db.session.get(Question, question_requested)
            question.process = 4
            db.session.merge(question)
            db.session.commit()

    def check_questions(questions, user_id, request_id):
        # 確認した結果をそれぞれのDBに書き込む
        for question_raw in questions:
            # 問題文の状態の変更
            question = db.session.get(Question, question_raw['id'])
            if question_raw['checked'] == '確認済み':
                process = 5
            elif question_raw['checked'] == '再提出依頼':
                process = 6

            question.process = process


            db.session.merge(question)
            db.session.commit()

            now = datetime.now()

            # recordにmessageを記録
            new_record = Record(
                user = user_id,
                question = question_raw['id'],
                process = process,
                message = question_raw['message'],
                executed_at = now
            )
            db.session.add(new_record)
            db.session.commit()
            
        # question_requestへの記録
        question_request = db.session.get(Question_Request, request_id)
        question_request.process = 5
        question_request.checked_by = user_id
        question_request.finished_at = now
        db.session.merge(question_request)
        db.session.commit()
