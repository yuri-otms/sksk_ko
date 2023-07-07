from datetime import datetime
from flask import Blueprint, redirect, url_for, render_template, \
    request, flash, session
from flask_login import login_required
from sqlalchemy import or_

from sksk_app import db
from sksk_app.models import Grade, E_Group, Element, Question
import sksk_app.utils.approve as approval
import sksk_app.utils.edit as editor

approve = Blueprint('approve', __name__, url_prefix='/approve')

@approve.before_request
def load_logged_in_user():
    edit = session.get('approve')

    this_year = session.get('this_year')

    if not this_year:
       session['this_year'] = datetime.now().year

    if not edit:
        flash('アクセスが許可されていません')
        return redirect(url_for('pg.toppage'))
    
@approve.route('/')
@login_required
def index():
    return render_template('approve/index.html')

@approve.route('/question')
@login_required
def question():
    result = editor.EditManager.fetchAll()
    grade_id = result[0]
    e_group_id = result[1]
    element_id = result[2]

    grade = db.session.get(Grade, grade_id)
    e_group = db.session.get(E_Group, e_group_id)
    element = db.session.get(Element, element_id)
    grades = Grade.query.all()
    e_groups = E_Group.query.filter(E_Group.grade==grade_id)
    elements = Element.query.filter(Element.e_group==e_group_id)
    questions = Question.query.filter(Question.element==element_id)
    return render_template('approve/question.html', grade= grade, e_group=e_group, element=element, grades=grades, e_groups=e_groups, elements=elements, questions=questions, element_id=element_id)



@approve.route('/change/question')
@login_required
def change_question():
    question_id = request.args.get('q')
    question = db.session.get(Question, question_id)

    return render_template('approve/change_question.html', question=question)

@approve.route('/change/question_changed')
@login_required
def change_question_execute():
    question_id = request.args.get('q')
    user_id = session.get('user_id')
    approval.ReleaseManager.change_question_settings(user_id,question_id)

    question = db.session.get(Question, question_id)
    element_id = question.element
    return redirect(url_for('approve.change_question_done', e=element_id))

@approve.route('/change/question_changed_done')
@login_required
def change_question_done():
    element_id = request.args.get('e')
    flash('問題文の公開設定を変更しました。')
    return redirect(url_for('edit.show_questions', e=element_id))


@approve.route('/release/questions', methods=['POST'])
@login_required
def release_questions():
   
    if request.form.getlist('question'):
        releases = request.form.getlist('question')
    else:
        flash('問題が選択されていません。')
        return redirect(url_for('approve.not_approved_questions'))
    # 「全て選択」の選択を削除
    if releases[0] == 'on':
        releases.pop(0)
    questions = []
    for release in releases:
        question = db.session.get(Question, release)
        questions.append(question)

    return render_template('approve/release_questions.html', questions=questions, releases=releases)


@approve.route('/release/questions_changed', methods=['GET'])
@login_required
def release_questions_execute():
    releases = request.args.getlist('releases')
    user_id = session.get('user_id')
    approval.ReleaseManager.release_questions(user_id,releases)

    return redirect(url_for('approve.release_questions_done'))

@approve.route('/release/questions_changed_done')
@login_required
def release_questions_done():
    flash('問題文を公開しました。')
    return redirect(url_for('approve.not_approved_questions'))


@approve.route('/unrelease/questions', methods=['POST'])
@login_required
def unrelease_questions():
    if request.form.getlist('question'):
        releases = request.form.getlist('question')
    else:
        flash('問題が選択されていません')
        return redirect(url_for('approve.approved_questions'))
    # 「全て選択」の選択を削除
    if releases[0] == 'on':
        releases.pop(0)
    questions = []
    for release in releases:
        question = db.session.get(Question, release)
        questions.append(question)

    return render_template('approve/unrelease_questions.html', questions=questions, releases=releases)

@approve.route('/unrelease/questions_changed', methods=['GET'])
@login_required
def unrelease_questions_execute():
    releases = request.args.getlist('releases')
    user_id = session.get('user_id')
    approval.ReleaseManager.unrelease_questions(user_id, releases)

    return redirect(url_for('approve.unrelease_questions_done'))

@approve.route('/unrelease/questions_changed_done')
@login_required
def unrelease_questions_done():
    flash('問題文を非公開しました。')
    return redirect(url_for('req.index'))

@approve.route('/not_approved/questions')
@login_required
def not_approved_questions():
    questions_raw = Question.query.filter(or_(Question.process==5, Question.process==9)).order_by(Question.id)

    questions = []
    for question_raw in questions_raw:
        question = editor.QuestionManager.fetch_question_with_attribute(question_raw.id)
        questions.append(question)

    return render_template('approve/not_approved_questions.html', questions=questions)

@approve.route('/approved/questions')
@login_required
def approved_questions():
    edited_questions = Question.query.with_entities(Question.id, Grade.grade, Element.element, Question.japanese, Question.foreign_l).join(Element).join(E_Group).join(Grade).filter(Question.process==8).order_by(Question.id)
    return render_template('approve/approved_questions.html', questions=edited_questions)




    