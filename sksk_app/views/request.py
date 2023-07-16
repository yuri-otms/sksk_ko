from flask import Blueprint, redirect, url_for, render_template, session, flash, request
from flask_login import login_required
from datetime import datetime
from sqlalchemy import func, or_

from sksk_app import db
from sksk_app.models import Grade, E_Group, Element,Question, Question_Request,Requested_Question, Record
import sksk_app.utils.edit as editor
from sksk_app.utils.request import RequestManager


req = Blueprint('req', __name__, url_prefix='/request')

@req.before_request
def load_logged_in_user():
    edit = session.get('edit')
    check = session.get('check')
    approve = session.get('approve')
    
    this_year = session.get('this_year')

    if not this_year:
       session['this_year'] = datetime.now().year

    if not (edit or check or approve):
        flash('アクセスが許可されていません')
        return redirect(url_for('pg.toppage'))

@req.route('/')
@login_required
def index():
    user_id = session.get('user_id')
    requests_not_yet = Question_Request.query.filter(Question_Request.client==user_id).filter(Question_Request.finished_at==None).filter(Question_Request.process==4)
    
    requests_not_checked = Question_Request.query.filter(Question_Request.process==4)
    
    # 編集ユーザから見た完了依頼
    requests_done = RequestManager.fetch_checked_request_with_result(user_id)

    # 確認ユーザから見た完了依頼
    requests_checked = Question_Request.query.filter(Question_Request.checked_by==user_id).filter(Question_Request.process==5)

    # 承認待ちの完了依頼
    requests_not_approved = Question_Request.query.filter(Question_Request.process==5)

    return render_template('request/index.html',requests_not_yet=requests_not_yet, requests_not_checked=requests_not_checked, requests_done=requests_done, requests_checked=requests_checked, requests_not_approved=requests_not_approved)

@req.route('/not_checked')
@login_required
def not_checked_questions():

    user_id = session.get('user_id')
    edited_questions = Question.query.with_entities(Question.id, Grade.grade, Element.element, Question.japanese, Question.foreign_l).join(Element).join(E_Group).join(Grade).filter(Question.created_by==user_id).filter(or_(Question.process==1, Question.process==2))

    return render_template('request/not_checked_questions.html', questions=edited_questions)

@req.route('/request_check', methods=['POST'])
@login_required
def request_check():
    checks = request.form.getlist('question')
    if checks == []:
        flash('問題が選択されていません。')
        return redirect(url_for('req.not_checked_questions'))
    title = request.form['title']
    detail = request.form['detail']
    if checks[0] == 'on':
        checks.pop(0)
    questions = []
    for check in checks:
        question = Question.query.with_entities(Question.id, Grade.grade, Element.element, Question.japanese, Question.foreign_l).join(Element).join(E_Group).join(Grade).filter(Question.id==check).first()
        questions.append(question)

    # return render_template('request/request_check.html', checks=checks)
    
    return render_template('request/request_check.html', questions=questions, title=title, detail=detail)


@req.route('/request_check_requested', methods=['POST'])
@login_required
def request_check_execute():
    questions_requested = request.form.getlist('question_id')
    title = request.form['title']
    detail = request.form['detail']
    user_id = session.get('user_id')

    RequestManager.add_request(questions_requested, title, detail, user_id, 0)

    return redirect(url_for('req.request_check_done'))

@req.route('/request_check_requested_done')
@login_required
def request_check_done():
    flash('問題文の確認を依頼しました。')
    return redirect(url_for('req.index'))

@req.route('/delete/check_request', methods=['POST'])
@login_required
def delete_check_request():
    request_id = request.form['request_id']
    question_request = db.session.get(Question_Request, request_id)
    questions = RequestManager.fetch_questions_with_check_message(request_id)

    return render_template('request/delete_check_request.html', request=question_request, questions=questions)

@req.route('/delete/check_request_deleted', methods=['POST'])
@login_required
def delete_check_request_execute():
    request_id = request.form['request_id']
    RequestManager.delete_request(request_id)

    return redirect(url_for('req.delete_check_request_done'))

@req.route('/delete/check_request_deleted')
@login_required
def delete_check_request_done():
    flash('確認依頼を削除しました。')
    return redirect(url_for('req.index'))

@req.route('/resubmit/check_request')
@login_required
def resubmit_check_request():
    request_id = request.args.get('r')
    question_request = db.session.get(Question_Request, request_id)
    questions = RequestManager.fetch_rejected_questions_with_check_message(request_id)

    # 却下された問題のみを表示する

    return render_template('request/resubmit_check_request.html', request=question_request, questions=questions)

@req.route('/resubmit/check_request_check', methods=['POST'])
@login_required
def resubmit_check_request_check():
    request_id = request.form['request_id']
    question_request = db.session.get(Question_Request, request_id)

    title = request.form['title']
    detail = request.form['detail']

    questions = RequestManager.fetch_rejected_questions_with_check_message(request_id)

    return render_template('request/resubmit_check_request_check.html',request=question_request, title=title, detail=detail, questions=questions)

@req.route('/resubmit/check_request_resubmitted', methods=['POST'])
@login_required
def resubmit_check_request_execute():
    request_id = request.form['request_id']

    title = request.form['title']
    detail = request.form['detail']
    user_id = session.get('user_id')

    questions = RequestManager.search_rejected_question(request_id)

    RequestManager.add_request(questions, title, detail, user_id, request_id)


    return redirect(url_for('req.resubmit_check_request_done'))

@req.route('/resubmit/check_request_done')
@login_required
def resubmit_check_request_done():
    flash('確認依頼を再提出しました')
    return redirect(url_for('req.index'))

@req.route('/questions/requested')
@login_required
def show_requested_questions():
    request_id = request.args.get('r')
    question_request = db.session.get(Question_Request, request_id)
    questions = RequestManager.fetch_questions_with_check_message(request_id)
    rejected_questions = RequestManager.search_rejected_question(request_id)

    return render_template('request/requested_questions.html', request=question_request, questions=questions, rejected_questions = rejected_questions)

@req.route('/question/checked', methods=['POST'])
@login_required
def question_checked():
    request_id = request.form['request_id']
    question_request = db.session.get(Question_Request, request_id)

    questions_id = request.form.getlist('questions')
    checked_conditions = request.form.getlist('checked')
    messages = request.form.getlist('message')

    questions = RequestManager.fetch_checked_question_infomation(questions_id, checked_conditions, messages)

    return render_template('request/question_checked.html', questions=questions, request=question_request,checked_conditions=checked_conditions,messages=messages)

@req.route('/question/checked_execute', methods=['POST'])
@login_required
def question_checked_execute():
    request_id = request.form['request_id']
    user_id = session.get('user_id')

    questions_id = request.form.getlist('questions')
    checked_conditions = request.form.getlist('checked')
    messages = request.form.getlist('message')

    questions = RequestManager.fetch_checked_question_infomation(questions_id, checked_conditions, messages)

    RequestManager.check_questions(questions, user_id, request_id)
 
    return redirect(url_for('req.question_checked_done'))

@req.route('/question/checked_done')
@login_required
def question_checked_done():
    flash('問題文の確認を行いました。')
    return redirect(url_for('req.index'))





