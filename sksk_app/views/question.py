import math
from flask import Blueprint, redirect, url_for, render_template, session, request
from flask_login import login_required
from sqlalchemy import not_, func

from sksk_app import db
from sksk_app.models import Grade, E_Group, Element, Question, Score
import sksk_app.utils.edit as editor
import sksk_app.utils.user as user_setting

question = Blueprint('question', __name__, url_prefix='/question')

@question.route('/select_element')
@login_required
def select_element():
    result = editor.EditManager.fetchAll()
    grade_id = result[0]
    e_group_id = result[1]

    grades = db.session.query(Grade).all()
    e_groups = editor.EditManager.addE_GroupName(grade_id)

    grade = db.session.get(Grade, grade_id)
    e_group = db.session.get(E_Group, e_group_id)
    grade_position = grade.position
    e_group_position = e_group.position

    elements = Element.query.filter(Element.e_group==e_group_id)

    return render_template('question/element.html', grades=grades, e_groups=e_groups, grade_position=grade_position, e_group_position=e_group_position, elements=elements)

@question.route('/element/<int:id>', methods=['GET'])
@login_required
def show_first_question(id):
    user_id = session['user_id']
    no = 1
    #1周目の問題の取得(5問)
    answered_question = Score.query.with_entities(Score.question).filter(Score.user==user_id)
    questions_raw = Question.query.filter(Question.element==id).filter(Question.id.not_in(answered_question)).order_by(Question.id.asc()).limit(5).all()

    if not questions_raw:
        #2周目以降の問題を取得(5問)
        questions_raw = Score.query.with_entities(Question.id,func.count(Score.question).label('count')).join(Question).filter(Question.element==id).filter(Score.user==user_id).group_by(Score.question).order_by('count', func.lpad((Question.id), 6, 0)).limit(5).all()

    questions = []
    for question in questions_raw:
        questions.append([question.id, 0])
    session['questions'] = questions

    question = editor.QuestionManager.fetch_question_with_hints(questions[0][0])
    attribute = editor.QuestionManager.fetch_attribute(question['element'])

    return render_template('question/question.html', question=question, no=no, attribute=attribute)

@question.route('/question/record', methods=['POST'])
@login_required
def record_score():
    no = int(request.form['no'])
    correct = int(request.form['correct'])
    questions = session.get('questions')
    user_id = session.get('user_id')

    index = no - 1
    questions[index][1] = correct
    session['questions'] = questions

    user_setting.ScoreManager.add_score(user_id, questions[index][0], correct, 0)
    
    if no < len(questions):
        return redirect(url_for('question.show_question', no=no), code=307)
    else:
        return redirect(url_for('question.finish', questions=questions, no=no), code=307)
    
@question.route('/question', methods=['POST'])
@login_required
def show_question():
    no = int(request.form['no'])
    questions = session.get('questions')
    question = editor.QuestionManager.fetch_question_with_hints(questions[no][0])
    no += 1

    attribute = editor.QuestionManager.fetch_attribute(question['element'])

    return render_template('question/question.html', question=question, no=no, attribute=attribute)

@question.route('/question/finish', methods=['POST'])
@login_required
def finish():
    no = int(request.form['no'])
    questions = session.get('questions')

    correct_answer = 0

    for question in questions:
        if question[1] == 1:
            correct_answer += 1

    correct_ratio = math.floor((correct_answer/no)*100)

    return render_template('question/finish.html', no=no, correct_answer=correct_answer, correct_ratio=correct_ratio) 





        



