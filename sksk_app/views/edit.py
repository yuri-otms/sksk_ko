from flask import Blueprint, redirect, url_for, render_template, request, \
    flash, session
from flask_login import login_required
from sqlalchemy import func

from sksk_app import db
from sksk_app.models import Grade, E_Group, Element, Style, Question, Hint, Word
import sksk_app.utils.edit as editor
import sksk_app.utils.api as api

edit = Blueprint('edit', __name__, url_prefix='/edit')

@edit.before_request
def load_logged_in_user():
    edit = session.get('edit')

    if not edit:
        flash('アクセスが許可されていません')
        return redirect(url_for('pg.toppage'))

@edit.route('/index')
@login_required
def index():
    grade_id = editor.EditManager.fetch_grade()
    grade = db.session.get(Grade, grade_id)
    grade_position = grade.position
    grades = Grade.query.all()
    e_groups = E_Group.query.filter(E_Group.grade==grade_id)
    return render_template('edit/index.html', grade_id=grade_id, grades=grades, e_groups=e_groups, grade_position=grade_position)

@edit.route('/show', methods=['GET'])
@login_required
def show():
    #選択された項目グループの項目を表示
    result = editor.EditManager.fetchAll()
    grade_id = result[0]
    e_group_id = result[1]
    element_id = result[2]
    grade_id = editor.EditManager.fetch_grade()
    e_group_id = editor.EditManager.fetchE_Group(grade_id)

    grades = db.session.query(Grade).all()
    e_groups = editor.EditManager.addE_GroupName(grade_id)

    e_group = db.session.get(E_Group, e_group_id)
    grade_id = e_group.grade
    grade = db.session.get(Grade, grade_id)
    grade_name = grade.grade
    grade_position = grade.position
    elements = Element.query.filter(Element.e_group==e_group_id)
    e_group_name = e_group.e_group
    e_group_position = e_group.position
    e_group_id = e_group.id


    return render_template('edit/show.html', grades = grades, e_groups=e_groups, elements=elements,grade_name=grade_name, grade_id=grade_id, grade_position = grade_position,e_group_position=e_group_position,e_group_name=e_group_name, e_group_id=e_group_id)

@edit.route('/show/questions', methods=['GET'])
def show_questions():
    result = editor.EditManager.fetchAll()
    grade_id = result[0]
    e_group_id = result[1]
    element_id = result[2]
        
    element = db.session.get(Element, element_id)

    grade = db.session.get(Grade, grade_id)
    grade_position = grade.position

    e_group_id = editor.EditManager.fetchE_Group(grade_id)
    e_group_position = db.session.get(E_Group, e_group_id).position
    grades = Grade.query.all()
    e_groups = E_Group.query.filter(E_Group.grade==grade_id)
    styles = Style.query.all()

    elements = Element.query.filter(Element.e_group==e_group_id)

    questions_raw = Question.query.filter(Question.element==element.id)
    questions = []
    for question in questions_raw:
        style = db.session.get(Style, question.style)
        one_question = {
            "id":question.id,
            "japanese":question.japanese,
            "foreign_l":question.foreign_l,
            "style": style.style,
            "position":question.position
        }
        questions.append(one_question)

    return render_template('edit/show_questions.html',grade_id=grade_id, grade_position= grade_position, e_group_position=e_group_position, grades=grades, e_groups=e_groups, styles=styles, e_group_id=e_group_id, elements=elements, element=element, questions=questions)

@edit.route('/show/hints', methods=['GET'])
def show_hints():
    result = editor.EditManager.fetchAll()
    grade_id = result[0]
    e_group_id = result[1]
    element_id = result[2]
        
    element = db.session.get(Element, element_id)

    grade = db.session.get(Grade, grade_id)
    grade_position = grade.position

    e_group_id = editor.EditManager.fetchE_Group(grade_id)
    e_group_position = db.session.get(E_Group, e_group_id).position
    grades = Grade.query.all()
    e_groups = E_Group.query.filter(E_Group.grade==grade_id)
    styles = Style.query.all()

    elements = Element.query.filter(Element.e_group==e_group_id)

    questions_with_hints = editor.QuestionManager.fetch_questions_with_hints(element.id)

    return render_template('edit/show_hints.html',grade_id=grade_id, grade_position= grade_position, e_group_position=e_group_position, grades=grades, e_groups=e_groups, styles=styles, e_group_id=e_group_id, elements=elements, element=element, questions=questions_with_hints)


@edit.route('/add/grade', methods=['POST'])
@login_required
def add_grade():
    grade_name = request.form['grade']
    description = request.form['description']
    position = request.form['position']

    grade = Grade(
        grade = grade_name,
        description = description,
        position = position
    
    )

    return render_template('edit/add_grade.html', grade = grade)


@edit.route('/add/grade_added', methods=['POST'])
@login_required
def add_grade_execute():
    grade = request.form['grade']
    description = request.form['description']
    position = request.form['position']
    editor.GradeManager.add_grade(grade, description, position)
    # レベルを追加すると同時にグループを1つ追加する。
    grade_id = Grade.query.filter(Grade.grade== grade).first().id
    e_group = '新規グループ'
    description = '新規グループ'
    position = 1
    editor.E_GroupManager.add_e_group(grade_id, e_group, description, position)
    # 項目グループを追加すると同時に項目を1つ追加する。
    e_group_id = E_Group.query.filter(E_Group.e_group==e_group).first().id
    element = '新規項目'
    description = '新規項目'
    position = 1
    editor.ElementManager.add_element(e_group_id, element, description, position)
    

    return redirect(url_for('edit.add_grade_done'))



@edit.route('/add/grade/done')
@login_required
def add_grade_done():
    flash('レベルを登録を行いました。')

    return redirect(url_for('edit.show'))

@edit.route('/add/e_group', methods=['POST'])
@login_required
def add_e_group():
    grade_id = request.form['grade']
    e_group = request.form['e_group_name']
    description = request.form['description']
    position = request.form['position']

    grade = db.session.get(Grade, grade_id)
    e_group = E_Group(
        grade = grade,
        e_group = e_group,
        description = description,
        position = position
    )

    return render_template('edit/add_e_group.html', e_group=e_group, grade_name=grade.grade)

@edit.route('/add/e_groupe_added', methods=['POST'])
@login_required
def add_e_group_execute():
    grade_id = request.form['grade']
    e_group = request.form['e_group']
    description = request.form['description']
    position = request.form['position']

    editor.E_GroupManager.add_e_group(grade_id, e_group, description, position)
    # 項目グループを追加すると同時に項目を1つ追加する。
    e_group_id = E_Group.query.filter(E_Group.e_group==e_group).first().id
    element = '項目1'
    description = '一つ目の項目'
    position = 1
    editor.ElementManager.add_element(e_group_id, element, description, position)

    return redirect(url_for('edit.add_e_group_done', l=grade_id))

@edit.route('/add/e_group_added_done')
@login_required
def add_e_group_done():
    grade_id = request.args.get('l')
    flash('項目グループを登録しました')
    return redirect(url_for('edit.show', l=grade_id))


# 項目の追加
@edit.route('/add/element', methods=['POST'])
@login_required
def add_element():
    e_group_id = request.form['e_group_id']
    element_name = request.form['element_name']
    description = request.form['description']
    position = request.form['position']

    e_group = db.session.get(E_Group, e_group_id)
    e_group_name=e_group.e_group
    element = Element(
        e_group = e_group_id,
        element = element_name,
        description = description,
        position = position
    )

    return render_template('edit/add_element.html', element=element, e_group_name=e_group_name)

@edit.route('/add/element_added', methods=['POST'])
@login_required
def add_element_execute():
    e_group_id = request.form['e_group']
    element_name= request.form['element_name']
    description = request.form['description']
    position = request.form['position']

    editor.ElementManager.add_element(e_group_id, element_name, description, position)

    grade_id = db.session.get(E_Group, e_group_id).grade

    return redirect(url_for('edit.add_element_done', l=grade_id, g=e_group_id))

@edit.route('/add/element_added_done')
@login_required
def add_element_done():
    grade_id = request.args.get('l')
    e_group_id = request.args.get('g')
    flash('項目を登録しました')
    return redirect(url_for('edit.show', l=grade_id, g=e_group_id))

@edit.route('/add/question', methods=['POST'])
@login_required
def add_question():
    japanese = request.form['japanese1']
    foreign_l = request.form['foreign_l1']
    style_id = request.form['style']
    position = request.form['position']
    element_id = request.form['element_id']

    style = db.session.get(Style, style_id)
    element = db.session.get(Element, element_id)
    e_group = db.session.get(E_Group, element.e_group)
    grade = db.session.get(Grade, e_group.grade)

    ja_to_ko = api.Papago.ja_to_ko(japanese)
    ko_to_ja = api.Papago.ko_to_ja(foreign_l)

    question = {
        "grade":grade.grade,
        "e_group":e_group.e_group,
        "element_id":element.id,
        "element": element.element,
        "japanese": japanese,
        "ja_to_ko": ja_to_ko,
        "foreign_l": foreign_l,
        "ko_to_ja":ko_to_ja,
        "style_id": style.id,
        "style":style.style,
        "position": position,
    }

    return render_template('edit/add_question.html', question=question)

@edit.route('/add/question_added', methods=['POST'])
@login_required
def add_question_execute():
    element = request.form['element']
    level = 1
    japanese1 = request.form['japanese1']
    foreign_l1 = request.form['foreign_l1']
    style = request.form['style']
    position = request.form['position']
    user = session.get('user_id')

    editor.QuestionManager.add_question(element, level, japanese1, foreign_l1, style, position, user)

    return redirect(url_for('edit.add_question_done', e=element))

@edit.route('/add/question_added_done')
@login_required
def add_question_done():
    element = request.args.get('e')
    flash('問題文を追加しました。')

    return redirect(url_for('edit.show_questions', e=element))

@edit.route('/confirm/hint/j', methods=['POST'])
@login_required
def confirm_hint_j():
    question_id = request.form['question_id']
    j_word = request.form['j_word']
    question_with_hints = editor.QuestionManager.fetch_question_with_components_hints(question_id)

    j_words = Word.query.filter(Word.japanese.like("%" + j_word + "%"))
    translated_word = api.Papago.ja_to_ko(j_word)

    words = editor.HintManager.fetch_word(question_id)
    hint_existed = editor.HintManager.confirm_j_hint(question_id, j_word)

    return render_template('edit/confirm_hint_j.html', question=question_with_hints, j_word=j_word, j_words=j_words, translated_word=translated_word, words=words, hint_existed=hint_existed)

@edit.route('/confirm/hint/f', methods=['POST'])
@login_required
def confirm_hint_f():
    question_id = request.form['question_id']
    f_word = request.form['f_word']
    question_with_hints = editor.QuestionManager.fetch_question_with_components_hints(question_id)

    f_words = Word.query.filter(Word.japanese.like("%" + f_word + "%"))
    translated_word = api.Papago.ko_to_ja(f_word)

    words = editor.HintManager.fetch_word(question_id)
    hint_existed = editor.HintManager.confirm_f_hint(question_id, f_word)

    return render_template('edit/confirm_hint_f.html', question=question_with_hints, f_word=f_word, f_words=f_words, translated_word=translated_word, words=words, hint_existed=hint_existed)

@edit.route('/add/word/hint', methods=['POST'])
@login_required
def add_word_hint():
    question_id = request.form['question_id']
    j_word = request.form['j_word']
    f_word = request.form['f_word']
    question_with_hints = editor.QuestionManager.fetch_question_with_components_hints(question_id)

    return render_template('edit/add_hint.html', question = question_with_hints, j_word=j_word, f_word=f_word)

@edit.route('/add/word/hint_addded', methods=['POST'])
@login_required
def add_word_hint_execute():
    question_id = request.form['question_id']
    j_word = request.form['j_word']
    f_word = request.form['f_word']

    editor.WordManager.add_word(j_word, f_word)
    word_id = Word.query.filter(Word.japanese==j_word).filter(Word.foreign_l==f_word).first().id
    editor.HintManager.add_hint(question_id, word_id)
    question = db.session.get(Question, question_id)
    element = db.session.get(Element, question.element)

    return redirect(url_for('edit.add_word_hint_done', e=element.id))

@edit.route('/add/word/hint_addded_done', methods=['GET'])
@login_required
def add_word_hint_done():
    element = request.args.get('e')
    flash('単語とヒントを追加しました')
    return redirect(url_for('edit.show_hints', e=element))

@edit.route('/delete/question/<int:id>')
@login_required
def delete_question(id):

    question = editor.QuestionManager.fetch_question_with_attribute(id)

    return render_template('edit/delete_question.html', question=question)

@edit.route('/delete/question_deleted', methods=['POST'])
@login_required
def delete_question_execute():
    element_id = request.form['element_id']
    question_id = request.form['question_id']

    editor.QuestionManager.delete_question(question_id)

    return redirect(url_for('edit.delete_question_done', e=element_id))

@edit.route('/delete/question_deleted_done')
@login_required
def delete_question_done():
    element_id = request.args.get('e')
    flash('問題文を削除しました。')
    return redirect(url_for('edit.show_questions', e=element_id))