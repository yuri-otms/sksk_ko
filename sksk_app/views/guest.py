from flask import Blueprint, redirect, url_for, render_template, request,session
import numpy
import math

from sksk_app import db
from sksk_app.models import Grade, E_Group, Element, Question, Hint, Word
import sksk_app.utils.edit as editor

guest = Blueprint('guest', __name__, url_prefix='/guest')

@guest.route('/select_grade')
def select_grade():
    grades = Grade.query.filter(Grade.released==1)
    return render_template('guest/grades.html', grades=grades)

@guest.route('/select_e_group')
def select_e_group():
    grade_id = request.args.get('grade')
    e_groups = E_Group.query.filter(E_Group.released==1).filter(E_Group.grade==grade_id)
    return render_template('guest/e_groups.html', e_groups=e_groups)

@guest.route('/select_element')
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

    return render_template('guest/element.html', grades=grades, e_groups=e_groups, elements=elements, grade_position=grade_position, e_group_position=e_group_position)

# 問題文の表示
@guest.route('/element/<int:id>', methods=['GET'])
def show_first_question(id):
    no = 1



    questions_raw = Question.query.filter(Question.element==id).filter(Question.released==1).order_by(Question.position.asc()).limit(5).all()
    question = questions_raw[0]
    question = editor.QuestionManager.fetch_question_with_hints(question.id)
    attribute = editor.QuestionManager.fetch_attribute(question['element'])
    questions = []
    for question_raw in questions_raw:
        questions.append([question_raw.id, 0])

    session['questions'] = questions

    return render_template('guest/question.html', question=question, no=no, attribute=attribute)

@guest.route('/question/record', methods=['POST'])
def record_score():
    no = int(request.form['no'])
    correct = int(request.form['correct'])
    questions = session.get('questions')

    index = no -1
    questions[index][1] = correct
    session['questions'] = questions

    if no < len(questions):
        return redirect(url_for('guest.show_question', no=no), code=307)
    else:
        return redirect(url_for('guest.finish', questions=questions, no=no), code=307)

@guest.route('/question', methods=['POST'])
def show_question():
    questions = session.get('questions')
    no = int(request.form['no'])
    question = editor.QuestionManager.fetch_question_with_hints(questions[no][0])
    no += 1

    attribute = editor.QuestionManager.fetch_attribute(question['element'])

    return render_template('guest/question.html', question=question, no=no, attribute=attribute)

@guest.route('/question/finish', methods=['POST'])
def finish():
    questions = session.get('questions')
    no = int(request.form['no'])

    correct_answer = 0

    for question in questions:
        if question[1] == 1:
            correct_answer += 1

    correct_ratio = math.floor((correct_answer/no)*100)

    return render_template('guest/finish.html', no=no, correct_answer=correct_answer, correct_ratio=correct_ratio)


