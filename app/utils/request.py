from flask import request
from sqlalchemy import func, or_
from datetime import datetime

from app import db
from models.grade import Grade
from models.e_group import E_Group
from models.element import Element
from models.question import Question
from models.word import Word
from models.hint import Hint
from models.style import Style
from models.record import Record
from models.score import Score
from models.requested_question import Requested_Question
from models.question_request import Question_Request

class RequestManager:

    def fetch_checked_question_infomation(questions_id, checked_conditions, messages):
        questions_raw = []
        for question_id in questions_id:
            question = Question.query.with_entities(Question.id, Grade.grade, Element.element, Question.japanese, Question.foreign_l).join(Element).join(E_Group).join(Grade).filter(Question.id==question_id).first()
            questions_raw.append(question)

        questions = []
        index = 0
        for question_raw in questions_raw:

            if checked_conditions:
                for checked_condition in checked_conditions:
                    if question_raw.id == int(checked_condition):
                        checked = "確認済み"
                        break
                    else:
                        checked = "再提出依頼"
            else:
                checked="再提出依頼"

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

        question_request = db.session.get(Question_Request, request_id)

        questions = []
        for question_raw in questions_raw:
            if question_request.process == 5 or question_request.process == 6:
                record = Record.query.filter(Record.question==question_raw.id).filter(or_(Record.process==5, Record.process==6)).order_by(Record.id.desc()).first()
                message = record.message
                if record.process == 5:
                    process_name = '確認済み'
                elif record.process == 6:
                    process_name = '確認却下'
                else:
                    process_name = ''
            else:
                process_name = ''
                message = ''
                

            question = {
                "id": question_raw.id,
                "grade": question_raw.grade,
                "element": question_raw.element,
                "japanese": question_raw.japanese,
                "foreign_l": question_raw.foreign_l,
                "checked": process_name,
                "message": message
            }
            questions.append(question)

        return questions

    def fetch_rejected_questions_with_check_message(request_id):

        rejected_questions = RequestManager.search_rejected_question(request_id)

        questions = []
        for rejected_question in rejected_questions:
            record = Record.query.filter(Record.question==rejected_question).order_by(Record.id.desc()).first()
            question_raw = Question.query.with_entities(Question.id, Grade.grade, Element.element, Element.id.label('element_id'),Question.japanese, Question.foreign_l).join(Element).join(E_Group).join(Grade).filter(Question.id==rejected_question).first()

            question = {
                "id": question_raw.id,
                "grade": question_raw.grade,
                "element": question_raw.element,
                "element_id": question_raw.element_id,
                "japanese": question_raw.japanese,
                "foreign_l": question_raw.foreign_l,
                "message": record.message
            }
            questions.append(question)

        return questions
    

    def search_rejected_question(request_id):
        # 却下された問題があるか探す
        rejected_questions = []
        requested_questions = Question.query.join(Requested_Question).filter(Requested_Question.request_id==request_id)
        for requested_question in requested_questions:
            record = Record.query.filter(Record.question==requested_question.id).order_by(Record.id.desc()).first()
            if record.process == 6:
                rejected_questions.append(record.question)
                
        return rejected_questions
    
    def fetch_checked_request_with_result(user_id):
        requests_done_raw = Question_Request.query.filter(Question_Request.client==user_id).filter(Question_Request.process==5)

        requests_done = []
        for request_done_raw in requests_done_raw:
            # 却下された問題があるか探す
            condition = 0
            rejected_questions = RequestManager.search_rejected_question(request_done_raw.id)
            if rejected_questions:
                condition = 1
                resubmit = Question_Request.query.filter(Question_Request.id==request_done_raw.id).filter(Question_Request.request_id==0).first()
                if not resubmit:
                    condition = 2
            
            request_done = {
                "id":request_done_raw.id,
                "client":request_done_raw.client,
                "process":request_done_raw.process,
                "title":request_done_raw.title,
                "detail":request_done_raw.detail,
                "requested_at":request_done_raw.requested_at,
                "checked_by":request_done_raw.checked_by,
                "finished_at":request_done_raw.finished_at,
                "condition":condition
            }

            requests_done.append(request_done)

        return requests_done


    # 確認依頼
    def add_request(questions_requested, title, detail, user_id, request_id):
        now = datetime.now()

        new_request = Question_Request(
            client = user_id,
            process = 4,
            title = title,
            detail = detail,
            requested_at = now,
            request_id = request_id
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

    def edit_request(request_id, title, detail, questions):

        question_request = db.session.get(Question_Request, request_id)
        question_request.title = title
        question_request.detail = detail

        db.session.merge(question_request)
        db.session.commit()

    def remove_questions_from_request(request_id, questions):

        for question in questions:
            requested_question = Requested_Question.query.filter(Requested_Question.request_id==request_id).filter(Requested_Question.question==int(question)).first()
            db.session.delete(requested_question)
            db.session.commit()

    def delete_request(request_id):

        question_request = db.session.get(Question_Request, request_id)
        question_request.process = 3
        db.session.merge(question_request)
        db.session.commit()

        requested_questions = Question.query.join(Requested_Question).filter(Requested_Question.request_id==request_id)
        for requested_question in requested_questions:
            question = db.session.get(Question, requested_question.id)
            question.process = 2
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
