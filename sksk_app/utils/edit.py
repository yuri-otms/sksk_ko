from flask import request
from sqlalchemy import func
from datetime import datetime
import glob

import MeCab
from konlpy.tag import Okt

from sksk_app import db
from sksk_app.models import Grade, E_Group, Element, Question, Word, Hint, Style, Record, Score

class GradeManager:
    def add_grade(grade, description):
        grades = Grade.query.all()
        if grades:
            max_position = db.session.query(
                func.max(Grade.position).label('grade_max')).one()
            max = int(max_position.grade_max)
            position = max + 1
        else:
            position = 1

        new_grade = Grade(
            grade = grade,
            description = description,
            position = position
        )
        
        db.session.add(new_grade)
        db.session.commit()

    def edit_grade(id, grade, description):
        grade_edited = db.session.get(Grade, id)

        grade_edited.grade = grade
        grade_edited.description = description

        db.session.merge(grade_edited)
        db.session.commit()

    def delete_grade(id):
        grade_deleted = db.session.get(Grade, id)

        db.session.delete(grade_deleted)
        db.session.commit()


class E_GroupManager:

    def calculate_position(grade_id):
        e_group_exist = E_Group.query.filter(E_Group.grade==grade_id).first()
        if e_group_exist:
            max_position = E_Group.query.with_entities(func.max(E_Group.position).label('e_group_max')).filter(E_Group.grade==grade_id).one()
            max = int(max_position.e_group_max)
            position = max + 1
        else:
            position = 1
        
        return position

    # 削除した項目グループ以降の項目グループの項番の変更
    def reduce_position(e_group_id):
        e_group = db.session.get(E_Group, e_group_id)
        grade = e_group.grade
        position = e_group.position

        next_e_group = E_Group.query.filter(E_Group.grade==grade).filter(E_Group.position>position).order_by(E_Group.position).first()
        while(next_e_group):
            next_e_group.position -= 1
            position = next_e_group.position
            db.session.merge(next_e_group)
            db.session.commit()
            next_e_group = E_Group.query.filter(E_Group.grade==grade).filter(E_Group.position>position).order_by(E_Group.position).first()

    def add_e_group(grade, e_group, description):
        position = E_GroupManager.calculate_position(grade)
        new_e_group = E_Group(
            grade = grade,
            e_group = e_group,
            description = description,
            position = position
        )
        db.session.add(new_e_group)
        db.session.commit()

    def edit_e_group(e_group_id, grade_id, e_group_name, description):
        e_group = db.session.get(E_Group, e_group_id)
        grade_before = e_group.grade
        
        if not grade_id == grade_before:
            E_GroupManager.reduce_position(e_group_id)
            position = E_GroupManager.calculate_position(grade_id)
            e_group.position = position
        e_group.e_group = e_group_name
        e_group.description = description
        e_group.grade = grade_id
        db.session.merge(e_group)
        db.session.commit()


    def delete_e_group(e_group_id):
        E_GroupManager.reduce_position(e_group_id)
        e_group = db.session.get(E_Group, e_group_id)
        db.session.delete(e_group)
        db.session.commit()



class ElementManager:

    def calculate_position(e_group_id):
        element_exist = Element.query.filter(Element.e_group==e_group_id).first()
        if element_exist:
            max_position = Element.query.with_entities(func.max(Element.position).label('element_max')).filter(Element.e_group==e_group_id).one()
            max = int(max_position.element_max)
            position = max + 1
        else:
            position = 1

        return position

    def reduce_position(element_id):
        element = db.session.get(Element, element_id)
        e_group = element.e_group
        position = element.position

        next_element = Element.query.filter(Element.e_group==e_group).filter(Element.position>position).order_by(Element.position).first()
        while(next_element):
            next_element.position -= 1
            position = next_element.position
            db.session.merge(next_element)
            db.session.commit()
            next_element = Element.query.filter(Element.e_group==e_group).filter(Element.position>position).order_by(Element.position).first()

    def add_element(e_group_id, element, description):
        position = ElementManager.calculate_position(e_group_id)

        new_element = Element(
            e_group = e_group_id,
            element = element,
            description = description,
            position = position
        )

        db.session.add(new_element)
        db.session.commit()

    def edit_element(element_id, e_group_id, element_name, description):
        element = db.session.get(Element, element_id)
        e_group_before = element.e_group

        if e_group_id != e_group_before:
            ElementManager.reduce_position(element_id)
            position = ElementManager.calculate_position(e_group_id)
            element.position = position
        
        element.element = element_name
        element.description = description
        element.e_group = e_group_id

        db.session.merge(element)
        db.session.commit()


    def delete_element(element_id):
        element = db.session.get(Element, element_id)
        ElementManager.reduce_position(element_id)
        db.session.delete(element)
        db.session.commit()
    
class StyleManager:
    def add_style(style):
        new_style = Style(
            style = style
        )

        db.session.add(new_style)
        db.session.commit()

class QuestionManager:
    
    def calculate_position(element):

        question_exist = Question.query.filter(Question.element==element).first()
        if question_exist:
            max_position = Question.query.with_entities(func.max(Question.position).label('question_max')).filter(Question.element==element).filter(Question.process!=3).one()
            max = int(max_position.question_max)
            position = max + 1
        else:
            position = 1

        return position        

    def reduce_position(question_id):
        question = db.session.get(Question, question_id)
        element = question.element
        position = question.position

        next_question = Question.query.filter(Question.element==element).filter(Question.position>position).filter(Question.process!=3).order_by(Question.position).first()
        while(next_question):
            next_question.position -= 1
            position = next_question.position
            db.session.merge(next_question)
            db.session.commit()
            next_question = Question.query.filter(Question.element==element).filter(Question.position>position).filter(Question.process!=3).order_by(Question.position).first()


    def add_question(element, level,  japanese, foreign_l, style, spoken, sida, will, user):

        position = QuestionManager.calculate_position(element)
        created_at = datetime.now()
        
        new_question = Question(
            element = element,
            level = level,
            japanese = japanese,
            foreign_l = foreign_l,
            style = style,
            spoken = spoken,
            sida = sida,
            will = will,
            position = position,
            created_at = created_at,
            created_by = user,
            process = 1
        )

        db.session.add(new_question)
        db.session.commit()

        question_id = Question.query.with_entities(func.max(Question.id).label('max_id')).one().max_id

        message = ''
        QuestionManager.record_process(user, question_id, 1,message, created_at)

    def edit_question(question_id, element, japanese, foreign_l, style, spoken, sida, will, user, request_id):
        created_at = datetime.now()

        question = db.session.get(Question, question_id)

        element_before = question.element
        
        if element == element_before:
            question.position = question.position
        else:
            QuestionManager.reduce_position(question_id)
            position = QuestionManager.calculate_position(element)
            question.position = position

        question.element = element
        question.japanese = japanese
        question.foreign_l = foreign_l
        question.style = style
        question.spoken = spoken
        question.sida = sida
        question.will = will 

        db.session.merge(question)
        db.session.commit()


        if request_id:
            message = '再提出のための編集'
            QuestionManager.record_process(user, question_id, 6, message, created_at)
        else:
            message = ''
            QuestionManager.record_process(user, question_id, 2, message, created_at)
        
    
    def delete_question(question_id, user):
        QuestionManager.reduce_position(question_id)

        created_at = datetime.now()

        question = db.session.get(Question, question_id)
        question.process = 3
        db.session.merge(question)
        db.session.commit()
        
        message = ''
        QuestionManager.record_process(user, question_id, 3, message, created_at)


    def record_process(user, question, process, message, time):
        new_record = Record(
            user = user,
            question = question,
            process = process,
            message = message,
            executed_at = time
        )
        db.session.add(new_record)
        db.session.commit()

    def fetch_questions_with_hints(element):
        questions = Question.query.filter(Question.element==element).filter(Question.process!=3)
        questions_with_hints = []
        i = 0
        mecab = MeCab.Tagger()
        for question in questions:
            question_with_hints = {
            'id': question.id,
            'japanese':question.japanese,
            'foreign_l':question.foreign_l,
            'word':None,
            'foword':None,
            'hint':None
            }
            questions_with_hints.append(question_with_hints)

            # 単語の候補
            questions_with_hints[i]['japanese_word']= []
            node = mecab.parseToNode(questions_with_hints[i]['japanese'])
            while node:
                p = node.feature.split(',')[0]
                if p == '名詞' or p == '動詞' or p== '形容詞' or p =='副詞':
                    questions_with_hints[i]['japanese_word'].append(node.feature.split(",")[6])
                node = node.next


            # 韓国語のそれぞれの単語
            questions_with_hints[i]['foreign_word'] = []
            text = questions_with_hints[i]['foreign_l']
            okt = Okt()
            korean_w = okt.morphs(text, norm=True, stem=True)
            for w in korean_w:
                questions_with_hints[i]['foreign_word'].append(w)

            # 登録済みのヒント
            hints = Hint.query.filter(Hint.question==question.id)
            questions_with_hints[i]['hint']= []
            for hint in hints:
                word = db.session.get(Word, hint.word)
                questions_with_hints[i]['hint'].append(word)
            i += 1

        return questions_with_hints
    
    def fetch_question_with_components_hints(question_id):
        question = db.session.get(Question, question_id)
        question_with_hints = {
            'id': int(question.id),
            'japanese':question.japanese,
            'foreign_l':question.foreign_l,
            'element':question.element,
            'japanese_word':None,
            'foreign_word':None,
            'hint':None
        }
        mecab = MeCab.Tagger()
        # 単語の候補
        question_with_hints['japanese_word']= []
        node = mecab.parseToNode(question_with_hints['japanese'])
        while node:
            p = node.feature.split(',')[0]
            if p == '名詞' or p == '動詞' or p== '形容詞' or p =='副詞':
                question_with_hints['japanese_word'].append(node.feature.split(",")[6])
            node = node.next

        # 韓国語のそれぞれの単語
        question_with_hints['foreign_word'] = []
        text = question_with_hints['foreign_l']
        okt = Okt()
        korean_w = okt.morphs(text, norm=True, stem=True)
        for word in korean_w:
            question_with_hints['foreign_word'].append(word)


        # 登録済みのヒント
        hints = Hint.query.filter(Hint.question==question.id)
        question_with_hints['hint']= []
        for hint in hints:
            word = db.session.get(Word, hint.word)
            question_with_hints['hint'].append(word)

        return question_with_hints
    
    def fetch_question_with_hints(question_id):
        question = db.session.get(Question, question_id)
        style = db.session.get(Style, question.style)
        question_with_hints = {
            'id': int(question.id),
            'japanese':question.japanese,
            'foreign_l':question.foreign_l,
            'element':question.element,
            'hint':None,
            'style_id':question.style,
            'style':style.style,
            'spoken':question.spoken,
            'sida':question.sida,
            'will':question.will
        }

        # 登録済みのヒント
        hints = Hint.query.filter(Hint.question==question.id)
        question_with_hints['hint']= []
        for hint in hints:
            word = db.session.get(Word, hint.word)
            question_with_hints['hint'].append(word)

        return question_with_hints
    
    def fetch_attribute(element):
        element = db.session.get(Element, element)
        e_group = db.session.get(E_Group, element.e_group)
        grade = db.session.get(Grade, e_group.grade)

        attribute = {
            "element":element.element,
            "description":element.description,
            "e_group":e_group.e_group,
            "grade":grade.grade
        }
        return attribute
    
    def fetch_question_with_attribute(question_id):

        question = db.session.get(Question, question_id)

        style = db.session.get(Style, question.style)
        element = db.session.get(Element, question.element)
        e_group = db.session.get(E_Group, element.e_group)
        grade = db.session.get(Grade, e_group.grade)
        
        file = 0
        file_name = 'sksk_app/static/audio/' + str(question.id).zfill(5) + '.mp3'
        if  glob.glob(file_name):
            file = 1

        question_added = {
            "id":question.id,
            "grade":grade.grade,
            "e_group":e_group.e_group,
            "element_id":element.id,
            "element": element.element,
            "japanese": question.japanese,
            "foreign_l": question.foreign_l,
            "style_id": style.id,
            "style":style.style,
            "spoken":int(question.spoken),
            "sida":int(question.sida),
            "will":int(question.will),
            "position": question.position,
            "audio":file
        }

        return question_added
    

class WordManager:

    def add_word(japanese_word, foreign_word):
        new_word = Word(
            japanese = japanese_word,
            foreign_l = foreign_word
        )

        db.session.add(new_word)
        db.session.commit()

    def edit_word(word_id, japanese_word, foreign_word):
        word = db.session.get(Word, word_id)
        word.japanese = japanese_word
        word.foreign_l = foreign_word

        db.session.merge(word)
        db.session.commit()

    def delete_word(word_id):
        word = db.session.get(Word, word_id)
        db.session.delete(word)
        db.session.commit()


class HintManager:

    #該当の問題文の単語の日本語・外国語の取得
    def fetch_word(question):

        hints = Hint.query.filter(Hint.question==question)
        words = []
        for hint in hints:
            word = db.session.get(Word, hint.word)
            words.append(word)

        return words

    def confirm_j_hint(question, japanese_word):
        hints = Hint.query.filter(Hint.question==question)
        existed = 0
        for hint in hints:
            word = db.session.get(Word, hint.word)
            if japanese_word in word.japanese:
                existed += 1
        
        return existed
    
    def confirm_f_hint(question, foreign_word):
        hints = Hint.query.filter(Hint.question==question)
        existed = 0
        for hint in hints:
            word = db.session.get(Word, hint.word)
            if foreign_word in word.foreign_l:
                existed += 1
        
        return existed
    
    def add_hint(question, word):
        new_hint = Hint(
            question = question,
            word = word
        )

        db.session.add(new_hint)
        db.session.commit()     

    def delete_hint(question_id, word_id):
        hint = Hint.query.filter(Hint.question==question_id).filter(Hint.word==word_id).first()
        db.session.delete(hint)
        db.session.commit()

class EditManager:
    
    def fetch_grade():
        if request.args.get('l'):
            grade_id = request.args.get('l')
        else:
            grade= Grade.query.with_entities(func.min(Grade.id).label('grade_min')).first()
            grade_id = grade.grade_min
        return grade_id

    def fetchE_Group(grade_id):
        if request.args.get('g'):
            e_group_id = request.args.get('g')
        else:
            e_group = E_Group.query.filter(E_Group.grade == grade_id).first()
            if e_group:
                e_group = E_Group.query.with_entities(E_Group.grade, func.min(E_Group.id).label('e_group_min')).filter(E_Group.grade==grade_id).group_by(E_Group.grade).one()
                e_group_id = e_group.e_group_min
            else:
                e_group_id = None
        return e_group_id
    
    def fetchElement(e_group_id):
        if request.args.get('e'):
            element_id = request.args.get('e')
        else:
            element = Element.query.filter(Element.e_group==e_group_id).first()
            if element:
                element = Element.query.with_entities(Element.e_group, func.min(Element.id).label('element_min')).filter(Element.e_group==e_group_id).group_by(Element.e_group).one()
                element_id = element.element_min
            else:
                element_id = None
        return element_id
    
    def fetchAll():
        if request.args.get('l'):
            grade_id = EditManager.fetch_grade()
            e_group_id = EditManager.fetchE_Group(grade_id)
            element_id = EditManager.fetchElement(e_group_id)
        elif request.args.get('g'):
            e_group_id = request.args.get('g')
            grade_id = db.session.get(E_Group, e_group_id).grade
            element_id = EditManager.fetchElement(e_group_id)
        elif request.args.get('e'):
            element_id = request.args.get('e')
            e_group_id = db.session.get(Element, element_id).e_group
            grade_id = db.session.get(E_Group, e_group_id).grade
        else:
            grade_id = EditManager.fetch_grade()
            e_group_id = EditManager.fetchE_Group(grade_id)
            element_id = EditManager.fetchElement(e_group_id)

        return grade_id, e_group_id, element_id

    # 今後使わなければ削除
    def addE_GroupName(grade_id):
        e_groups_raw = db.session.query(E_Group).filter(E_Group.grade==grade_id)
        e_groups = []
        for e_group in e_groups_raw:
            grade_name = db.session.get(Grade, e_group.grade)
            e_group_added = {
                "id":e_group.id,
                "grade":e_group.grade,
                "grade_name":grade_name.grade,
                "e_group":e_group.e_group,
                "description":e_group.description,
                "position":e_group.position
            }
            e_groups.append(e_group_added)

        return e_groups
