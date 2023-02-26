from flask import Blueprint, redirect, url_for, render_template, \
    request, flash, session
from flask_login import login_required

from sksk_app import db
from sksk_app.models import Grade, E_Group, Element, Question
import sksk_app.utils.approve as approval
import sksk_app.utils.edit as editor

approve = Blueprint('approve', __name__, url_prefix='/approve')

@approve.before_request
def load_logged_in_user():
    edit = session.get('approve')

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
    element_id = request.form['element_id']
    questions = Question.query.filter(Question.element == element_id)
    releases = request.form.getlist('question')
    if releases[0] == 'on':
        releases.pop(0)
    questions = []
    for release in releases:
        question = db.session.get(Question, release)
        questions.append(question)

    return render_template('approve/release_questions.html', questions=questions, releases=releases, element_id=element_id)


@approve.route('/release/questions_changed', methods=['GET'])
@login_required
def release_questions_execute():
    element_id = request.args.get('element_id')
    releases = request.args.getlist('releases')
    user_id = session.get('user_id')
    approval.ReleaseManager.release_questions(user_id,releases)

    return redirect(url_for('approve.release_questions_done', e=element_id))

@approve.route('/release/questions_changed_done')
@login_required
def release_questions_done():
    element_id = request.args.get('e')
    flash('問題文を公開しました。')

    return redirect(url_for('edit.show_questions', e=element_id))


@approve.route('/unrelease/questions', methods=['POST'])
@login_required
def unrelease_questions():
    element_id = request.form['element_id']
    questions = Question.query.filter(Question.element == element_id)
    releases = request.form.getlist('question')
    if releases[0] == 'on':
        releases.pop(0)
    questions = []
    for release in releases:
        question = db.session.get(Question, release)
        questions.append(question)

    return render_template('approve/unrelease_questions.html', questions=questions, releases=releases,element_id=element_id )

@approve.route('/unrelease/questions_changed', methods=['GET'])
@login_required
def unrelease_questions_execute():
    element_id = request.args.get('element_id')
    releases = request.args.getlist('releases')
    user_id = session.get('user_id')
    approval.ReleaseManager.unrelease_questions(user_id, releases)

    return redirect(url_for('approve.unrelease_questions_done', e=element_id))

@approve.route('/unrelease/questions_changed_done')
@login_required
def unrelease_questions_done():
    element_id = request.args.get('e')
    flash('問題文を非公開しました。')
    return redirect(url_for('edit.show_questions', e=element_id))
    