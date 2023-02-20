from flask import Blueprint, redirect, url_for, render_template, \
    request, flash, session
from flask_login import login_required

from sksk_app import db
from sksk_app.models import Level, E_Group, Element, Question
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

@approve.route('/level')
@login_required
def level():
    levels = Level.query.all()
    return render_template('approve/level.html', levels=levels)

@approve.route('/change/level')
@login_required
def change_level():
    level_id = request.args.get('l')

    level = db.session.get(Level, level_id)
    return render_template('approve/change_level.html', level=level)

@approve.route('/change/level_changed', methods=['GET'])
@login_required
def change_level_execute():
    level_id = request.args.get('l')

    approval.ReleaseManager.change_level_settings(level_id)

    return redirect(url_for('approve.change_level_done'))

@approve.route('/change/level_changed_done')
@login_required
def change_level_done():
    flash('レベルの公開設定を変更しました')

    return redirect(url_for('approve.level'))


@approve.route('/e_group')
@login_required
def e_group():
    level_id = editor.EditManager.fetchLevel()
    levels = Level.query.all()
    level = db.session.get(Level, level_id)
    e_groups = E_Group.query.filter(E_Group.level==level_id)
    return render_template('approve/e_group.html', e_groups=e_groups, level = level, levels=levels)

@approve.route('/change/e_group')
@login_required
def change_e_group():
    e_group_id = request.args.get('g')
    e_group = db.session.get(E_Group, e_group_id)
    return render_template('approve/change_e_group.html', e_group=e_group)

@approve.route('/change/e_group_changed')
@login_required
def change_e_group_execute():
    e_group_id = request.args.get('g')
    approval.ReleaseManager.change_e_group_settings(e_group_id)

    e_group = db.session.get(E_Group, e_group_id)
    level = e_group.level
    return redirect(url_for('approve.change_e_group_done', l=level))

@approve.route('/change/e_group_changed_done')
@login_required
def change_e_group_done():
    level = request.args.get('l')
    flash('項目グループの公開設定を変更しました。')
    return redirect(url_for('approve.e_group', l= level))

@approve.route('/element')
@login_required
def element():
    result = editor.EditManager.fetchAll()
    level_id = result[0]
    e_group_id = result[1]

    level = db.session.get(Level, level_id)
    e_group = db.session.get(E_Group, e_group_id)
    levels = Level.query.all()
    e_groups = E_Group.query.filter(E_Group.level==level_id)
    elements = Element.query.filter(Element.e_group==e_group_id)


    return render_template('approve/element.html',  level=level, levels=levels, e_group=e_group, e_groups=e_groups, elements=elements)

@approve.route('/change/element')
@login_required
def change_element():
    element_id = request.args.get('e')
    element = db.session.get(Element, element_id)

    return render_template('approve/change_element.html', element=element)

@approve.route('/change/element_changed')
@login_required
def change_element_execute():
    element_id = request.args.get('e')
    approval.ReleaseManager.change_element_settings(element_id)

    element = db.session.get(Element, element_id)
    group_id = element.e_group

    return redirect(url_for('approve.change_element_done', g=group_id))


@approve.route('/change/element_changed_done')
@login_required
def change_element_done():
    group_id = request.args.get('g')
    flash('項目の公開設定を変更しました。')

    return redirect(url_for('approve.element', g=group_id))

@approve.route('/question')
@login_required
def question():
    result = editor.EditManager.fetchAll()
    level_id = result[0]
    e_group_id = result[1]
    element_id = result[2]

    level = db.session.get(Level, level_id)
    e_group = db.session.get(E_Group, e_group_id)
    element = db.session.get(Element, element_id)
    levels = Level.query.all()
    e_groups = E_Group.query.filter(E_Group.level==level_id)
    elements = Element.query.filter(Element.e_group==e_group_id)
    questions = Question.query.filter(Question.element==element_id)
    return render_template('approve/question.html', level= level, e_group=e_group, element=element, levels=levels, e_groups=e_groups, elements=elements, questions=questions)



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
    approval.ReleaseManager.change_question_settings(question_id)

    question = db.session.get(Question, question_id)
    element_id = question.element
    return redirect(url_for('approve.change_question_done', e=element_id))

@approve.route('/change/question_changed_done')
@login_required
def change_question_done():
    element_id = request.args.get('e')
    flash('問題文の公開設定を変更しました。')
    return redirect(url_for('approve.question', e=element_id))


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
    approval.ReleaseManager.release_questions(releases)

    return redirect(url_for('approve.release_questions_done', e=element_id))

@approve.route('/release/questions_changed_done')
@login_required
def release_questions_done():
    element_id = request.args.get('e')
    flash('問題文を公開しました。')

    return redirect(url_for('approve.question', e=element_id))


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
    element_id = request.args.get('e')
    releases = request.args.getlist('releases')
    approval.ReleaseManager.unrelease_questions(releases)

    return redirect(url_for('approve.unrelease_questions_done', e=element_id))

@approve.route('/unrelease/questions_changed_done')
@login_required
def unrelease_questions_done():
    element_id = request.args.get('e')
    flash('問題文を非公開しました。')
    return redirect(url_for('approve.question', e=element_id))
    