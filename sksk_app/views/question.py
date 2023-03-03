import math
from flask import Blueprint, redirect, url_for, render_template, session, request
from flask_login import login_required, current_user
from sqlalchemy import not_, func

from sksk_app import db
from sksk_app.models import Grade, E_Group, Element, Question, Score
import sksk_app.utils.edit as editor
import sksk_app.utils.user as user_setting

question = Blueprint('question', __name__, url_prefix='/question')

@question.route('/check_login')
def check_login():
    if current_user.is_authenticated:
        return redirect(url_for('question.confirm_login'))
    else:
        return redirect(url_for('question.login'))

@question.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user_setting.LoginManager.login(email, password)

        return redirect(url_for('question.check_login'))

    page_title = 'ログイン'
    return render_template('question/login.html', page_title=page_title)

@question.route('/confirm_login')
@login_required
def confirm_login():
    return redirect(url_for('question.select_element', guest=0))

@question.route('/select_element')
def select_element():
    guest = int(request.args.get('guest'))

    result = editor.EditManager.fetchAll()
    grade_id = result[0]
    e_group_id = result[1]

    grades = Grade.query.join(E_Group).join(Element).join(Question).filter(Question.released==1)
    e_groups = E_Group.query.join(Element).join(Question).filter(Question.released==1).filter(E_Group.grade==grade_id)

    grade = db.session.get(Grade, grade_id)
    e_group = db.session.get(E_Group, e_group_id)
    grade_position = grade.position
    e_group_position = e_group.position

    elements = Element.query.join(Question).filter(Element.e_group==e_group_id).filter(Question.released==1)

    return render_template('question/element.html', grades=grades, e_groups=e_groups, grade_position=grade_position, e_group_position=e_group_position, elements=elements, guest=guest)

@question.route('/element', methods=['GET'])
def show_first_question():
    element_id = request.args.get('e')
    guest = int(request.args.get('guest'))
    review = int(request.args.get('review'))
    no = 1

    if not review:
        if guest:
            questions_raw = Question.query.filter(Question.element==element_id).filter(Question.released==1).order_by(Question.position.asc()).limit(5).all()

        else:
            user_id = session['user_id']
            #1周目の問題の取得(5問)
            answered_question = Score.query.with_entities(Score.question).filter(Score.user==user_id)
            questions_raw = Question.query.filter(Question.element==element_id).filter(Question.id.not_in(answered_question)).filter(Question.released==1).order_by(Question.id.asc()).limit(5).all()

            if not questions_raw:
                #2周目以降の問題を取得(5問)
                questions_raw = Score.query.with_entities(Question.id,func.count(Score.question).label('count')).join(Question).filter(Question.element==element_id).filter(Score.user==user_id).group_by(Score.question).order_by('count', func.lpad((Question.id), 6, 0)).limit(5).all()

        questions = []
        for question in questions_raw:
            questions.append([question.id, 0])
        session['questions'] = questions
    questions = session.get('questions')

    question = editor.QuestionManager.fetch_question_with_hints(questions[0][0])
    attribute = editor.QuestionManager.fetch_attribute(question['element'])

    question_id = str(question['id'])
    audio_file = 'audio/' + question_id.zfill(5) + '.mp3'

    return render_template('question/question.html', question=question, no=no, attribute=attribute, guest=guest, review=review, audio_file=audio_file)

@question.route('/record_temp', methods=['POST'])
def record_score_temp():
    guest = int(request.form['guest'])
    no = int(request.form['no'])
    review = int(request.form['review'])
    correct = int(request.form['correct'])
    questions = session.get('questions')

    index = no -1
    questions[index][1] = correct
    session['questions'] = questions

    if no < len(questions):
        return redirect(url_for('question.show_question', no=no, guest=guest, review=review), code=307)
    else:
        return redirect(url_for('question.finish', questions=questions, no=no, guest=guest, review=review), code=307)

@question.route('/question/record', methods=['POST'])
@login_required
def record_score():
    guest = int(request.form['guest'])
    no = int(request.form['no'])
    review = int(request.form['review'])
    correct = int(request.form['correct'])
    questions = session.get('questions')
    user_id = session.get('user_id')

    index = no - 1
    questions[index][1] = correct
    session['questions'] = questions

    user_setting.ScoreManager.add_score(user_id, questions[index][0], correct, 0)
    
    if no < len(questions):
        return redirect(url_for('question.show_question', no=no, guest=guest, review=review), code=307)
    else:
        return redirect(url_for('question.finish', questions=questions, no=no, guest=guest, review=review), code=307)
    
@question.route('/question', methods=['POST'])
def show_question():
    guest = int(request.form['guest'])
    no = int(request.form['no'])
    review = int(request.form['review'])
    questions = session.get('questions')
    question = editor.QuestionManager.fetch_question_with_hints(questions[no][0])
    no += 1

    attribute = editor.QuestionManager.fetch_attribute(question['element'])

    question_id = str(question['id'])
    audio_file = 'audio/' + question_id.zfill(5) + '.mp3'

    return render_template('question/question.html', question=question, no=no, attribute=attribute, guest=guest, review=review, audio_file=audio_file)

@question.route('/question/finish', methods=['POST'])
def finish():
    guest = int(request.form['guest'])
    no = int(request.form['no'])
    review = int(request.form['review'])
    questions = session.get('questions')

    correct_answer = 0

    for question in questions:
        if question[1] == 1:
            correct_answer += 1

    correct_ratio = math.floor((correct_answer/no)*100)

    question = db.session.get(Question, questions[0][0])
    element = db.session.get(Element, question.element)

    next_element = Element.query.join(Question).filter(Element.e_group==element.e_group).filter(Element.position > element.position).filter(not_(Element.id==question.element)).filter(Question.released==1).first()

    return render_template('question/finish.html', no=no, correct_answer=correct_answer, correct_ratio=correct_ratio, guest=guest, next_element=next_element, review=review) 

@question.route('/review/element', methods=['GET'])
def start_review_element():
    guest = int(request.args.get('guest'))
    answered_questions = session.get('questions')
    questions = []
    for answered_question in answered_questions:
        if answered_question[1] == 0:
            questions.append([answered_question[0], 0])

    session['questions'] = questions
    review = 1
    # question = db.session.get(Question, questions[0][0])

    return redirect(url_for('question.show_first_question', e=1, guest=guest, review=review))



