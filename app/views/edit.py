from datetime import datetime
from flask import Blueprint, redirect, url_for, render_template, request, \
    flash, session, Markup
from flask_login import login_required
from sqlalchemy import func
import glob

from app import db
from app.models import Grade, E_Group, Element, Style, Question, Hint, Word, User
import app.utils.edit as editor
import app.utils.api as api

edit = Blueprint('edit', __name__, url_prefix='/edit')

@edit.before_request
def load_logged_in_user():
    edit = session.get('edit')

    this_year = session.get('this_year')

    if not this_year:
       session['this_year'] = datetime.now().year

    if not edit:
        flash('アクセスが許可されていません')
        return redirect(url_for('pg.toppage'))

@edit.route('/index')
@login_required
def index():
    #選択された項目グループの項目を表示
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

    return render_template('edit/index.html', grade=grade, grades=grades, e_group=e_group, e_groups=e_groups, element=element, elements=elements)

@edit.route('/show/elements', methods=['GET'])
@login_required
def show_elements():
    #選択された項目グループの項目を表示
    result = editor.EditManager.fetchAll()
    grade_id = result[0]
    e_group_id = result[1]

    grades = Grade.query.order_by(Grade.position.asc())
    e_groups = E_Group.query.filter(E_Group.grade==grade_id).order_by(E_Group.position.asc())

    e_group = db.session.get(E_Group, e_group_id)
    grade = db.session.get(Grade, grade_id)
    
    elements = Element.query.filter(Element.e_group==e_group_id).order_by(Element.position.asc())


    return render_template('edit/show_elements.html', grades = grades, e_groups=e_groups, elements=elements,grade=grade,e_group=e_group)

@edit.route('/show/grade')
@login_required
def show_grades():
    grades = Grade.query.order_by(Grade.position.asc())

    return render_template('edit/show_grades.html', grades=grades)

@edit.route('/show/e_group')
@login_required
def show_e_groups():
    result = editor.EditManager.fetchAll()
    grade_id = result[0]
    e_group_id = result[1]
    grades = Grade.query.order_by(Grade.position.asc())
    e_groups = E_Group.query.filter(E_Group.grade==grade_id).order_by(E_Group.position.asc())

    e_group = db.session.get(E_Group, e_group_id)
    grade = db.session.get(Grade, grade_id)

    return render_template('edit/show_e_groups.html', grades=grades, grade=grade,e_group=e_group, e_groups=e_groups)

@edit.route('/show/questions', methods=['GET'])
def show_questions():
    approve = session.get('approve')
    result = editor.EditManager.fetchAll()
    grade_id = result[0]
    e_group_id = result[1]
    element_id = result[2]
        
    element = db.session.get(Element, element_id)

    grade = db.session.get(Grade, grade_id)
    e_group = db.session.get(E_Group, e_group_id)
    grades = Grade.query.all()
    e_groups = E_Group.query.filter(E_Group.grade==grade_id)
    styles = Style.query.all()

    elements = Element.query.filter(Element.e_group==e_group_id)

    questions_raw = Question.query.filter(Question.element==element.id).filter(Question.process!=3).order_by(Question.position.asc())

    questions = []
    for question in questions_raw:
        style = db.session.get(Style, question.style)
        file = 0
        file_name = 'sksk_app/static/audio/' + str(question.id).zfill(5) + '.mp3'
        if  glob.glob(file_name):
            file = 1
        created_by = User.query.filter(User.id==question.created_by).first()
        one_question = {
            "id":question.id,
            "japanese":question.japanese,
            "foreign_l":question.foreign_l,
            "style": style.style,
            "position":question.position,
            "created_by":created_by.name,
            "process": question.process,
            "spoken":question.spoken,
            "sida":question.sida,
            "will":question.will,
            "audio":file
        }
        questions.append(one_question)

    return render_template('edit/show_questions.html',grade=grade, e_group=e_group, grades=grades, e_groups=e_groups, styles=styles, elements=elements, element=element, questions=questions, approve=approve)

@edit.route('/show/hints', methods=['GET'])
def show_hints():
    result = editor.EditManager.fetchAll()
    grade_id = result[0]
    e_group_id = result[1]
    element_id = result[2]
        

    element = db.session.get(Element, element_id)

    grade = db.session.get(Grade, grade_id)
    e_group = db.session.get(E_Group, e_group_id)

    grades = Grade.query.all()
    e_groups = E_Group.query.filter(E_Group.grade==grade_id)
    styles = Style.query.all()

    elements = Element.query.filter(Element.e_group==e_group_id)

    questions_with_hints = editor.QuestionManager.fetch_questions_with_hints(element.id)

    return render_template('edit/show_hints.html',grade=grade,e_group=e_group, grades=grades, e_groups=e_groups, styles=styles, e_group_id=e_group_id, elements=elements, element=element, questions=questions_with_hints)


@edit.route('/add/grade', methods=['POST'])
@login_required
def add_grade():
    grade_name = request.form['grade']
    description = request.form['description']

    grade = Grade(
        grade = grade_name,
        description = description
    
    )

    return render_template('edit/add_grade.html', grade = grade)


@edit.route('/add/grade_added', methods=['POST'])
@login_required
def add_grade_execute():
    grade = request.form['grade']
    description = request.form['description']
    editor.GradeManager.add_grade(grade, description)
    # レベルを追加すると同時にグループを1つ追加する。
    grade_id = Grade.query.filter(Grade.grade== grade).first().id
    e_group = '新規グループ'
    description = '新規グループ'
    editor.E_GroupManager.add_e_group(grade_id, e_group, description)
    # 項目グループを追加すると同時に項目を1つ追加する。
    e_group_id = E_Group.query.filter(E_Group.e_group==e_group).first().id
    element = '新規項目'
    description = '新規項目'
    position = 1
    editor.ElementManager.add_element(e_group_id, element, description)
    return redirect(url_for('edit.add_grade_done'))

@edit.route('/add/grade/done')
@login_required
def add_grade_done():
    flash('レベルを登録を行いました。')
    return redirect(url_for('edit.show_grades'))

@edit.route('/edit/grade')
@login_required
def edit_grade():
    grade_id = request.args.get('grade')
    grade = db.session.get(Grade, grade_id)
    return render_template('edit/edit_grade.html', grade=grade)

@edit.route('/edit/grade/check', methods=['POST'])
@login_required
def edit_grade_check():
    grade_id = request.form['grade_id']
    grade_name = request.form['grade_name']
    description = request.form['description']

    grade = {
        "id":grade_id,
        "grade":grade_name,
        "description": description
    }

    return render_template('edit/edit_grade_check.html', grade=grade)

@edit.route('/edit/grade_edited', methods=['POST'])
@login_required
def edit_grade_execute():
    grade_id = request.form['grade_id']
    grade_name = request.form['grade_name']
    description = request.form['description']

    editor.GradeManager.edit_grade(grade_id, grade_name, description)    
    return redirect(url_for('edit.edit_grade_done'))

@edit.route('/edit/grade_edited_done')
@login_required
def edit_grade_done():
    flash('級を変更しました')

    return redirect(url_for('edit.show_grades'))

@edit.route('/delete/grade')
@login_required
def delete_grade():
    grade_id = request.args.get('grade')
    grade = db.session.get(Grade, grade_id)
    return render_template('edit/delete_grade.html', grade=grade)

@edit.route('/delete/grade_deleted', methods=['POST'])
@login_required
def delete_grade_execute():
    grade_id = request.form['grade_id']

    editor.GradeManager.delete_grade(grade_id)
    return redirect(url_for('edit.delete_grade_done'))

@edit.route('/delete/grade_deleted_done')
@login_required
def delete_grade_done():
    flash('級を削除しました。')
    return redirect(url_for('edit.show_grades'))

@edit.route('/add/e_group', methods=['POST'])
@login_required
def add_e_group():
    grade_id = request.form['grade']
    e_group = request.form['e_group_name']
    description = request.form['description']

    grade = db.session.get(Grade, grade_id)
    e_group = E_Group(
        grade = grade,
        e_group = e_group,
        description = description
    )

    return render_template('edit/add_e_group.html', e_group=e_group, grade_name=grade.grade)

@edit.route('/add/e_groupe_added', methods=['POST'])
@login_required
def add_e_group_execute():
    grade_id = request.form['grade']
    e_group = request.form['e_group']
    description = request.form['description']

    editor.E_GroupManager.add_e_group(grade_id, e_group, description)
    # 項目グループを追加すると同時に項目を1つ追加する。
    e_group_id = E_Group.query.filter(E_Group.e_group==e_group).first().id
    element = '項目1'
    description = '一つ目の項目'
    editor.ElementManager.add_element(e_group_id, element, description)

    return redirect(url_for('edit.add_e_group_done', l=grade_id))

@edit.route('/add/e_group_added_done')
@login_required
def add_e_group_done():
    grade_id = request.args.get('l')
    flash('項目グループを登録しました')
    return redirect(url_for('edit.show_e_groups', l=grade_id))

@edit.route('/edit/e_group')
@login_required
def edit_e_group():
    e_group_id = request.args.get('e_group')
    grade_id = editor.EditManager.fetch_grade()
    e_group = db.session.get(E_Group, e_group_id)
    grade = db.session.get(Grade, grade_id)
    grades = Grade.query.all()
    return render_template('edit/edit_e_group.html', e_group=e_group, grade=grade,grades=grades)

@edit.route('/edit/e_group_check', methods=['POST'])
@login_required
def edit_e_group_check():
    e_group_id = request.form['e_group_id']
    e_group_name = request.form['e_group']
    description = request.form['description']
    grade_id = request.form['grade_id']

    e_group = {
        "id": e_group_id,
        "e_group": e_group_name,
        "description": description
    }

    grade = db.session.get(Grade, grade_id)
    return render_template('edit/edit_e_group_check.html', e_group=e_group, grade=grade)

@edit.route('/edit/e_group_edited', methods=['POST'])
@login_required
def edit_e_group_execute():
    e_group_id = request.form['e_group_id']
    e_group_name = request.form['e_group_name']
    description = request.form['description']
    grade_id = int(request.form['grade_id'])

    editor.E_GroupManager.edit_e_group(e_group_id, grade_id, e_group_name, description) 

    return redirect(url_for('edit.edit_e_group_done', g=e_group_id))

@edit.route('/edit/e_group_edited_done')
@login_required
def edit_e_group_done():
    e_group_id = request.args.get('g')
    flash('項目グループを変更しました。')
    return redirect(url_for('edit.show_e_groups', g=e_group_id))

@edit.route('/delete/e_group')
@login_required
def delete_e_group():
    e_group_id = request.args.get('e_group')
    e_group = db.session.get(E_Group, e_group_id)
    grade = db.session.get(Grade, e_group.grade)

    return render_template('edit/delete_e_group.html', e_group=e_group, grade=grade)

@edit.route('/delete/e_group_deleted', methods=['POST'])
@login_required
def delete_e_group_execute():
    e_group_id = request.form['e_group']

    e_group = db.session.get(E_Group, e_group_id)
    editor.E_GroupManager.delete_e_group(e_group_id)

    return redirect(url_for('edit.delete_e_group_done', l=e_group.grade))

@edit.route('/delete/e_group_deleted_done')
@login_required
def delete_e_group_done():
    grade_id = request.args.get('l')
    flash('項目グループを削除しました。')

    return redirect(url_for('edit.show_e_groups', l=grade_id))


# 項目の追加
@edit.route('/add/element', methods=['POST'])
@login_required
def add_element():
    e_group_id = request.form['e_group_id']
    element_name = request.form['element_name']
    description = request.form['description']

    e_group = db.session.get(E_Group, e_group_id)
    e_group_name=e_group.e_group
    element = Element(
        e_group = e_group_id,
        element = element_name,
        description = description
    )

    return render_template('edit/add_element.html', element=element, e_group_name=e_group_name)

@edit.route('/add/element_added', methods=['POST'])
@login_required
def add_element_execute():
    e_group_id = request.form['e_group']
    element_name= request.form['element_name']
    description = request.form['description']

    editor.ElementManager.add_element(e_group_id, element_name, description)

    grade_id = db.session.get(E_Group, e_group_id).grade

    return redirect(url_for('edit.add_element_done', l=grade_id, g=e_group_id))

@edit.route('/add/element_added_done')
@login_required
def add_element_done():
    grade_id = request.args.get('l')
    e_group_id = request.args.get('g')
    flash('項目を登録しました')
    return redirect(url_for('edit.show_elements', l=grade_id, g=e_group_id))


@edit.route('/edit/element')
@login_required
def edit_element():
    result = editor.EditManager.fetchAll()
    grade_id = result[0]
    e_group_id = result[1]

    element_id = request.args.get('e')

    element = db.session.get(Element, element_id)
    e_group = db.session.get(E_Group, e_group_id)
    grade = db.session.get(Grade, grade_id)

    grades = Grade.query.all()
    e_groups = E_Group.query.filter(E_Group.grade==grade_id)

    return render_template('edit/edit_element.html', element=element,grade=grade, e_group=e_group, grades=grades, e_groups=e_groups)


@edit.route('/edit/element_check', methods=['POST'])
@login_required
def edit_element_check():
    element_id = request.form['element_id']
    element_name = request.form['element_name']
    description = request.form['description']
    e_group_id = request.form['e_group_id']

    e_group = db.session.get(E_Group, e_group_id)
    grade = db.session.get(Grade, e_group.grade)

    element = {
        "id":element_id,
        "e_group_id":e_group_id,
        "element":element_name,
        "description":description
    }

    return render_template('edit/edit_element_check.html', element=element, e_group=e_group, grade=grade)

@edit.route('/edit/element_edited', methods=['POST'])
@login_required
def edit_element_execute():
    element_id = request.form['element_id']
    element_name = request.form['element_name']
    description = request.form['description']
    e_group_id = int(request.form['e_group_id'])

    editor.ElementManager.edit_element(element_id, e_group_id, element_name, description)

    return redirect(url_for('edit.edit_element_done', g=e_group_id))

@edit.route('/edit/element_edited_done')
@login_required
def edit_element_done():
    e_group_id = request.args.get('g')
    flash('項目を変更しました。')
    return redirect(url_for('edit.show_elements', g=e_group_id))

@edit.route('/delete/element')
@login_required
def delete_element():
    element_id = request.args.get('element_id')
    element = db.session.get(Element, element_id)
    e_group = db.session.get(E_Group, element.e_group)
    return render_template('edit/delete_element.html', element = element, e_group=e_group)

@edit.route('/delete/element_deleted', methods=['POST'])
@login_required
def delete_element_execute():
    element_id = request.form['element_id']
    e_group_id = request.form['e_group_id']

    editor.ElementManager.delete_element(element_id)

    return redirect(url_for('edit.delete_element_done', g=e_group_id))

@edit.route('/delete/element_deleted_done')
@login_required
def delete_element_done():
    e_group_id = request.args.get('g')
    return redirect(url_for('edit.show_elements', g=e_group_id))

# 質問の追加・編集・削除
@edit.route('/add/question', methods=['POST'])
@login_required
def add_question():
    element_id = request.form['element_id']
    element = db.session.get(Element, element_id)
    e_group = db.session.get(E_Group, element.e_group)
    grade = db.session.get(Grade, e_group.grade)
    questions = []


    message_no_korean = Markup('韓国語文が入力されていません。<br><button class="add" style="font-size:0.9em;" type="button" onclick="history.back()">入力した内容を復旧する</button>')
    message_no_japanese = Markup('日本語文が入力されていません。<br><button class="add" style="font-size:0.9em;" type="button" onclick="history.back()">入力した内容を復旧する</button>')

    # 全ての欄が空欄の場合
    if not request.form['japanese1'] and not request.form['japanese2'] and not request.form['japanese3'] and not request.form['japanese4'] and not request.form['japanese5'] and not request.form['foreign_l1'] and not request.form['foreign_l2'] and not request.form['foreign_l3'] and not request.form['foreign_l4'] and not request.form['foreign_l5'] :
        flash('問題文が入力されていません')
        return redirect(url_for('edit.show_questions', e=element_id))
    
    # 韓国語文のみ入力されて日本語文が空欄の場合
    if request.form['foreign_l1'] and not request.form['japanese1']:
        flash(message_no_japanese)
        return redirect(url_for('edit.show_questions', e=element_id))
    if request.form['foreign_l2'] and not request.form['japanese2']:
        flash(message_no_japanese)
        return redirect(url_for('edit.show_questions', e=element_id))
    if request.form['foreign_l3'] and not request.form['japanese3']:
        flash(message_no_japanese)
        return redirect(url_for('edit.show_questions', e=element_id))
    if request.form['foreign_l4'] and not request.form['japanese4']:
        flash(message_no_japanese)
        return redirect(url_for('edit.show_questions', e=element_id))
    if request.form['foreign_l5'] and not request.form['japanese5']:
        flash(message_no_japanese)
        return redirect(url_for('edit.show_questions', e=element_id))

    
    # 1つ目の問題文
    if request.form['japanese1']:
        japanese1 = request.form['japanese1']
        if request.form['foreign_l1']:
            foreign_l1 = request.form['foreign_l1']
        else:
            flash(message_no_korean)
            return redirect(url_for('edit.show_questions', e=element_id))
        style_id1 = request.form['style1']
        spoken1 = request.form['spoken1']
        sida1 = request.form['sida1']
        will1 = request.form['will1']

        style = db.session.get(Style, style_id1)

        ja_to_ko1 = api.Papago.ja_to_ko(japanese1)
        ko_to_ja1 = api.Papago.ko_to_ja(foreign_l1)

        question1 = {
            "grade":grade.grade,
            "e_group":e_group.e_group,
            "element_id":element.id,
            "element": element.element,
            "japanese": japanese1,
            "ja_to_ko": ja_to_ko1,
            "foreign_l": foreign_l1,
            "ko_to_ja":ko_to_ja1,
            "style_id": style.id,
            "style":style.style,
            "spoken":spoken1,
            "sida":sida1,
            "will":will1
        }
        questions.append(question1)

    # 2つ目の問題文
    if request.form['japanese2']:
        japanese2 = request.form['japanese2']
        if request.form['foreign_l2']:
            foreign_l1 = request.form['foreign_l2']
        else:
            flash(message_no_korean)
            return redirect(url_for('edit.show_questions', e=element_id))
        foreign_l2 = request.form['foreign_l2']
        style_id2 = request.form['style2']
        spoken2 = request.form['spoken2']
        sida2 = request.form['sida2']
        will2 = request.form['will2']

        style = db.session.get(Style, style_id2)

        ja_to_ko2 = api.Papago.ja_to_ko(japanese2)
        ko_to_ja2 = api.Papago.ko_to_ja(foreign_l2)

        question2 = {
            "grade":grade.grade,
            "e_group":e_group.e_group,
            "element_id":element.id,
            "element": element.element,
            "japanese": japanese2,
            "ja_to_ko": ja_to_ko2,
            "foreign_l": foreign_l2,
            "ko_to_ja":ko_to_ja2,
            "style_id": style.id,
            "style":style.style,
            "spoken":spoken2,
            "sida":sida2,
            "will":will2
        }
        questions.append(question2)

    # 3つ目の問題文
    if request.form['japanese3']:
        japanese3 = request.form['japanese3']
        if request.form['foreign_l3']:
            foreign_l1 = request.form['foreign_l3']
        else:
            flash(message_no_korean)
            return redirect(url_for('edit.show_questions', e=element_id))
        foreign_l3 = request.form['foreign_l3']
        style_id3 = request.form['style3']
        spoken3 = request.form['spoken3']
        sida3 = request.form['sida3']
        will3 = request.form['will3']

        style = db.session.get(Style, style_id3)

        ja_to_ko3 = api.Papago.ja_to_ko(japanese3)
        ko_to_ja3 = api.Papago.ko_to_ja(foreign_l3)

        question3 = {
            "grade":grade.grade,
            "e_group":e_group.e_group,
            "element_id":element.id,
            "element": element.element,
            "japanese": japanese3,
            "ja_to_ko": ja_to_ko3,
            "foreign_l": foreign_l3,
            "ko_to_ja":ko_to_ja3,
            "style_id": style.id,
            "style":style.style,
            "spoken":spoken3,
            "sida":sida3,
            "will":will3
        }
        questions.append(question3)
        
    # 4つ目の問題文
    if request.form['japanese4']:
        japanese4 = request.form['japanese4']
        if request.form['foreign_l4']:
            foreign_l1 = request.form['foreign_l4']
        else:
            flash(message_no_korean)
            return redirect(url_for('edit.show_questions', e=element_id))
        foreign_l4 = request.form['foreign_l4']
        style_id4 = request.form['style4']
        spoken4 = request.form['spoken4']
        sida4 = request.form['sida4']
        will4 = request.form['will4']

        style = db.session.get(Style, style_id4)

        ja_to_ko4 = api.Papago.ja_to_ko(japanese4)
        ko_to_ja4 = api.Papago.ko_to_ja(foreign_l4)

        question4 = {
            "grade":grade.grade,
            "e_group":e_group.e_group,
            "element_id":element.id,
            "element": element.element,
            "japanese": japanese4,
            "ja_to_ko": ja_to_ko4,
            "foreign_l": foreign_l4,
            "ko_to_ja":ko_to_ja4,
            "style_id": style.id,
            "style":style.style,
            "spoken":spoken4,
            "sida":sida4,
            "will":will4
        }
        questions.append(question4)

    # 5つ目の問題文
    if request.form['japanese5']:
        japanese5 = request.form['japanese5']
        if request.form['foreign_l5']:
            foreign_l1 = request.form['foreign_l5']
        else:
            flash(message_no_korean)
            return redirect(url_for('edit.show_questions', e=element_id))
        foreign_l5 = request.form['foreign_l5']
        style_id5 = request.form['style5']
        spoken5 = request.form['spoken5']
        sida5 = request.form['sida5']
        will5 = request.form['will5']

        style = db.session.get(Style, style_id5)

        ja_to_ko5 = api.Papago.ja_to_ko(japanese5)
        ko_to_ja5 = api.Papago.ko_to_ja(foreign_l5)

        question5 = {
            "grade":grade.grade,
            "e_group":e_group.e_group,
            "element_id":element.id,
            "element": element.element,
            "japanese": japanese5,
            "ja_to_ko": ja_to_ko5,
            "foreign_l": foreign_l5,
            "ko_to_ja":ko_to_ja5,
            "style_id": style.id,
            "style":style.style,
            "spoken":spoken5,
            "sida":sida5,
            "will":will5
        }
        questions.append(question5)

    return render_template('edit/add_question.html', questions=questions)

@edit.route('/add/question_added', methods=['POST'])
@login_required
def add_question_execute():
    element = request.form['element']
    level = 1

    if request.form['japanese1']:
        japanese1 = request.form['japanese1']
        foreign_l1 = request.form['foreign_l1']
        style1 = request.form['style1']
        spoken1 = int(request.form['spoken1'])
        sida1 = int(request.form['sida1'])
        will1 = int(request.form['will1'])
        user = session.get('user_id')

        editor.QuestionManager.add_question(element, level, japanese1, foreign_l1, style1, spoken1, sida1, will1, user)

    if request.form['japanese2']:
        japanese2 = request.form['japanese2']
        foreign_l2 = request.form['foreign_l2']
        style2 = request.form['style2']
        spoken2 = int(request.form['spoken2'])
        sida2 = int(request.form['sida2'])
        will2 = int(request.form['will2'])

        editor.QuestionManager.add_question(element, level, japanese2, foreign_l2, style2, spoken2, sida2, will2, user)


    if request.form['japanese3']:
        japanese3 = request.form['japanese3']
        foreign_l3 = request.form['foreign_l3']
        style3 = request.form['style3']
        spoken3 = int(request.form['spoken3'])
        sida3 = int(request.form['sida3'])
        will3 = int(request.form['will3'])

        editor.QuestionManager.add_question(element, level, japanese3, foreign_l3, style3, spoken3, sida3, will3, user)


    if request.form['japanese4']:
        japanese4 = request.form['japanese4']
        foreign_l4 = request.form['foreign_l4']
        style4 = request.form['style4']
        spoken4 = int(request.form['spoken4'])
        sida4 = int(request.form['sida4'])
        will4 = int(request.form['will4'])

        editor.QuestionManager.add_question(element, level, japanese4, foreign_l4, style4, spoken4, sida4, will4, user)

    
    if request.form['japanese5']:
        japanese5 = request.form['japanese5']
        foreign_l5 = request.form['foreign_l5']
        style5 = request.form['style5']
        spoken5 = int(request.form['spoken5'])
        sida5 = int(request.form['sida5'])
        will5 = int(request.form['will5'])

        editor.QuestionManager.add_question(element, level, japanese5, foreign_l5, style5, spoken5, sida5, will5, user)

    return redirect(url_for('edit.add_question_done', e=element))

@edit.route('/add/question_added_done')
@login_required
def add_question_done():
    element = request.args.get('e')
    flash('問題文を追加しました。')

    return redirect(url_for('edit.show_questions', e=element))

@edit.route('/edit/question')
@login_required
def edit_question():
    request_id = 0
    if request.args.get('r'):
        request_id = request.args.get('r')
    question_id = request.args.get('q')
    result = editor.EditManager.fetchAll()
    grade_id = result[0]
    e_group_id = result[1]
    element_id = result[2]
        
    element = db.session.get(Element, element_id)

    grade = db.session.get(Grade, grade_id)
    e_group = db.session.get(E_Group, e_group_id)
    grades = Grade.query.all()
    e_groups = E_Group.query.filter(E_Group.grade==grade_id)
    styles = Style.query.all()

    elements = Element.query.filter(Element.e_group==e_group_id)
    question = editor.QuestionManager.fetch_question_with_attribute(question_id)
    return render_template('edit/edit_question.html', question=question, grades=grades, e_groups=e_groups, grade=grade, e_group=e_group,element=element, styles=styles, elements=elements, request_id=request_id)

@edit.route('/edit/question/ckeck', methods=['POST'])
@login_required
def edit_question_check():
    request_id = request.form['request_id']
    japanese = request.form['japanese']
    foreign_l = request.form['foreign_l']
    style_id = request.form['style']
    spoken = int(request.form['spoken'])
    sida = int(request.form['sida'])
    will = int(request.form['will'])
    
    element_id = request.form['element']
    question_id = request.form['question_id']

    style = db.session.get(Style, style_id)
    element = db.session.get(Element, element_id)
    e_group = db.session.get(E_Group, element.e_group)
    grade = db.session.get(Grade, e_group.grade)

    ja_to_ko = api.Papago.ja_to_ko(japanese)
    ko_to_ja = api.Papago.ko_to_ja(foreign_l)

    question = {
        "id":question_id,
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
        "spoken":spoken,
        "sida":sida,
        "will":will
    }

    question_before = editor.QuestionManager.fetch_question_with_attribute(question_id)

    return render_template('edit/edit_question_check.html', question=question, question_before=question_before, request_id=request_id)

@edit.route('/edit/question_edited', methods=['POST'])
@login_required
def edit_question_execute():
    request_id = int(request.form['request_id'])
    question_id = request.form['question_id']
    element_id = int(request.form['element'])

    japanese = request.form['japanese']
    foreign_l = request.form['foreign_l']
    style_id = request.form['style']
    spoken = int(request.form['spoken'])
    sida = int(request.form['sida'])
    will = int(request.form['will'])

    user = session.get('user_id')

    editor.QuestionManager.edit_question(question_id, element_id, japanese, foreign_l, style_id, spoken, sida, will, user, request_id)
    
    return redirect(url_for('edit.edit_question_done', e=element_id, r=request_id))

@edit.route('/edit/question_edited_done')
@login_required
def edit_question_done():
    element_id = request.args.get('e')
    request_id = int(request.args.get('r'))
    flash('問題文を変更しました。')

    if request_id:
        return redirect(url_for('req.resubmit_check_request', r=request_id))
    else:
        return redirect(url_for('edit.show_questions', e=element_id))


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
    user = session.get('user_id')

    editor.QuestionManager.delete_question(question_id, user)

    return redirect(url_for('edit.delete_question_done', e=element_id))

@edit.route('/delete/question_deleted_done')
@login_required
def delete_question_done():
    element_id = request.args.get('e')
    flash('問題文を削除しました。')
    return redirect(url_for('edit.show_questions', e=element_id))

@edit.route('/confirm/hint/j', methods=['POST'])
@login_required
def confirm_hint_j():
    question_id = request.form['question_id']
    japanese_word = request.form['japanese_word']
    question_with_hints = editor.QuestionManager.fetch_question_with_components_hints(question_id)

    japanese_words = Word.query.filter(Word.japanese.like("%" + japanese_word + "%"))
    translated_word = api.Papago.ja_to_ko(japanese_word)

    words = editor.HintManager.fetch_word(question_id)
    hint_existed = editor.HintManager.confirm_j_hint(question_id, japanese_word)

    # return render_template('edit/confirm_hint_j.html')
    return render_template('edit/confirm_hint_j.html', question=question_with_hints, japanese_word=japanese_word, japanese_words=japanese_words, translated_word=translated_word, words=words, hint_existed=hint_existed)


@edit.route('/confirm/hint/f', methods=['POST'])
@login_required
def confirm_hint_f():
    question_id = request.form['question_id']
    foreign_word = request.form['foreign_word']
    question_with_hints = editor.QuestionManager.fetch_question_with_components_hints(question_id)

    foreign_words = Word.query.filter(Word.foreign_l.like("%" + foreign_word + "%"))
    translated_word = api.Papago.ko_to_ja(foreign_word)

    words = editor.HintManager.fetch_word(question_id)
    hint_existed = editor.HintManager.confirm_f_hint(question_id, foreign_word)

    return render_template('edit/confirm_hint_f.html', question=question_with_hints, foreign_word=foreign_word, foreign_words=foreign_words, translated_word=translated_word, words=words, hint_existed=hint_existed)

@edit.route('/add/word/hint', methods=['POST'])
@login_required
def add_word_hint():

    question_id = request.form['question_id']
    japanese_word = request.form['japanese_word']
    foreign_word = request.form['foreign_word']
    question_with_hints = editor.QuestionManager.fetch_question_with_components_hints(question_id)
    ja_to_ko = api.Papago.ja_to_ko(japanese_word)
    ko_to_ja = api.Papago.ko_to_ja(foreign_word)

    for hint in question_with_hints['hint']:
        if hint.foreign_l == foreign_word:
            flash('同じヒントが既に登録されています。')
            return redirect(url_for('edit.show_hints', e=question_with_hints['element']))

    return render_template('edit/add_word_hint.html', question = question_with_hints, japanese_word=japanese_word, foreign_word=foreign_word, ja_to_ko=ja_to_ko, ko_to_ja=ko_to_ja)

@edit.route('/add/word/hint_addded', methods=['POST'])
@login_required
def add_word_hint_execute():
    question_id = request.form['question_id']
    japanese_word = request.form['japanese_word']
    foreign_word = request.form['foreign_word']

    editor.WordManager.add_word(japanese_word, foreign_word)
    word_id = Word.query.filter(Word.japanese==japanese_word).filter(Word.foreign_l==foreign_word).first().id
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


@edit.route('/add//hint', methods=['GET'])
@login_required
def add_hint():
    question_id = request.args.get('q')
    word_id = request.args.get('w')

    question = db.session.get(Question, question_id)
    word = db.session.get(Word, word_id)

    
    question_with_hints = editor.QuestionManager.fetch_question_with_components_hints(question_id)

    for hint in question_with_hints['hint']:
        if hint.foreign_l == word.foreign_l:
            flash('同じヒントが既に登録されています。')
            return redirect(url_for('edit.show_hints', e=question_with_hints['element']))

    return render_template('edit/add_hint.html', question=question, word=word)

@edit.route('/add//hint_added', methods=['POST'])
@login_required
def add_hint_execute():
    element_id = request.form['element_id']
    question_id = request.form['question_id']
    word_id = request.form['word_id']

    editor.HintManager.add_hint(question_id, word_id)

    return redirect(url_for('edit.add_hint_done', e=element_id))

@edit.route('/add//hint_added_done', methods=['GET'])
@login_required
def add_hint_done():
    element_id = request.args.get('e')
    flash('ヒントを追加しました。')
    return redirect(url_for('edit.show_hints', e=element_id))


@edit.route('/add/word/hint/edit', methods=['POST'])
@login_required
def add_word_hint_edit():
    question_id = request.form['question_id']
    japanese_word = request.form['japanese_word']
    foreign_word = request.form['foreign_word']

    question = db.session.get(Question, question_id)

    return render_template('edit/add_hint_edit_word.html', question=question, japanese_word=japanese_word, foreign_word=foreign_word)

@edit.route('/edit/hint')
@login_required
def edit_hint():
    question_id = request.args.get('q')
    question =  editor.QuestionManager.fetch_question_with_hints(question_id)
    return render_template('edit/edit_hint.html', question=question)


@edit.route('/delete/hint')
@login_required
def delete_hint():
    question_id = request.args.get('q')
    word_id = request.args.get('w')
    question =  editor.QuestionManager.fetch_question_with_hints(question_id)
    word = db.session.get(Word, word_id)
    return render_template('edit/delete_hint.html', question=question, word=word)

@edit.route('/delete/hint_deleted', methods=['POST'])
@login_required
def delete_hint_execute():
    question_id = request.form['question_id']
    word_id = request.form['word_id']
    editor.HintManager.delete_hint(question_id, word_id)

    return redirect(url_for('edit.delete_hint_done', q=question_id))

@edit.route('/delete/hint_deleted_done')
@login_required
def delete_hint_done():
    question_id = request.args.get('q')
    flash('ヒントを削除しました。')
    return redirect(url_for('edit.edit_hint', q=question_id))

@edit.route('/create/audio_file')
@login_required
def create_audio_file():
    question_id = request.args.get('q')
    element_id = request.args.get('e')
    approve = int(request.args.get('a'))

    api.GoogleCloud.create_audio_file(question_id)

    return redirect(url_for('edit.create_audio_file_done', e=element_id, a=approve))

@edit.route('/create/audio_file_done')
@login_required
def create_audio_file_done():
    element_id = request.args.get('e')
    approve = int(request.args.get('a'))

    flash('音声ファイルを作成しました。')
    if approve:
        return redirect(url_for('approve.not_approved_questions'))
    else:
        return redirect(url_for('edit.show_questions', e=element_id))


@edit.route('/create/audio_files', methods=['POST'])
@login_required
def create_audio_files():
    element_id = request.form['element_id']
    releases = request.form.getlist('question')

    if not releases:
        flash('問題文の最低1つにチェックを入れてください')
        return redirect(url_for('edit.show_questions', e=element_id))

    # 「全て選択」の選択を削除
    if releases[0] == 'on':
        releases.pop(0)
    questions = []
    for release in releases:
        file_name = 'sksk_app/static/audio/' + str(release).zfill(5) + '.mp3'
        if  not glob.glob(file_name):
            question = db.session.get(Question, release)
            questions.append(question)
    
    releases = []
    for question in questions:
        releases.append(question.id)
    

    return render_template('edit/create_audio_files.html', questions=questions, element_id=element_id, releases=releases)


@edit.route('/create/audio_files_created')
@login_required
def create_audio_files_execute():
    element_id = request.args.get('e')
    releases = request.args.getlist('releases')
    for release in releases:
        api.GoogleCloud.create_audio_file(release)

    return redirect(url_for('edit.create_audio_files_done', e=element_id))

@edit.route('/create/audio_files_created_done')
@login_required
def create_audio_files_done():
    element_id = request.args.get('e')
    flash('音声ファイルを作成しました。')
    return redirect(url_for('edit.show_questions', e=element_id))

@edit.route('/word/show')
@login_required
def show_words():
    words = Word.query.all()
    return render_template('edit/show_words.html', words=words)

@edit.route('/edit/word')
@login_required
def edit_word():
    word_id = request.args.get('w')
    word = db.session.get(Word, word_id)

    translated_foreign_l = api.Papago.ko_to_ja(word.foreign_l)
    translated_japanese = api.Papago.ja_to_ko(word.japanese)

    questions = Question.query.join(Hint).filter(Hint.word==word_id)

    return render_template('edit/edit_word.html', word=word, translated_foreign_l=translated_foreign_l, translated_japanese=translated_japanese, questions=questions)

@edit.route('/edit/word/check', methods=['POST'])
@login_required
def edit_word_check():
    word_id = request.form['word_id']
    japanese = request.form['japanese']
    foreign_l = request.form['foreign_l']

    word = db.session.get(Word, word_id)

    return render_template('edit/edit_word_check.html', word=word, japanese=japanese, foreign_l=foreign_l)

@edit.route('/edit/word/execute', methods=['POST'])
@login_required
def edit_word_execute():
    word_id = request.form['word_id']
    japanese = request.form['japanese']
    foreign_l = request.form['foreign_l']

    editor.WordManager.edit_word(word_id, japanese, foreign_l)

    return redirect(url_for('edit.edit_word_done'))

@edit.route('/edit/word/done')
@login_required
def edit_word_done():
    flash('単語を変更しました。')
    return redirect(url_for('edit.show_words'))

@edit.route('/delete/word')
@login_required
def delete_word():
    word_id = request.args.get('w')
    word = db.session.get(Word, word_id)

    questions = Question.query.join(Hint).filter(Hint.word==word_id)

    return render_template('edit/delete_word.html', word=word, questions=questions)

@edit.route('/delete/word/execute', methods=['POST'])
@login_required
def delete_word_execute():
    word_id = request.form['word_id']

    editor.WordManager.delete_word(word_id)
    return redirect(url_for('edit.delete_word_done'))

@edit.route('/delete/word/done')
@login_required
def delete_word_done():
    flash('単語を削除しました。')
    return redirect(url_for('edit.show_words'))