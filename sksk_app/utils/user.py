from werkzeug.security import generate_password_hash
from datetime import datetime

from sksk_app import db
from sksk_app.models import User, Process, Score, Grade, E_Group, Element, Question


class UserManager:

    def register_user(name, email, password):
        regiestered_at = datetime.now()

        new_user = User(
            name = name,
            email = email,
            password = generate_password_hash(password, method='sha256'),
            registered_at = regiestered_at      
            )
        
        db.session.add(new_user)
        db.session.commit()

    def register_user_priv(name, email, password, edit, check, approve, admin):
        regiestered_at = datetime.now()

        new_user = User(
            name = name,
            email = email,
            password = generate_password_hash(password, method='sha256'),
            edit = edit,
            check = check,
            approve = approve,
            admin = admin,
            registered_at = regiestered_at      
            )
    
        db.session.add(new_user)
        db.session.commit()

    def delete_user(id):
        user = db.session.get(User, id)
        db.session.delete(user)
        db.session.commit()

    def edit_user(id, name, email, edit, check, approve, admin):

        user = db.session.get(User, id)

        user.name = name
        user.email = email
        user.edit = edit
        user.check = check
        user.approve = approve
        user.admin = admin

        db.session.merge(user)
        db.session.commit()

    def add_privilege(user, process):

        user = db.session.get(User, user)

        if process == 1:
            user.edit = True
        if process == 2:
            user.check = True
        if process == 3:
            user.approve = True
        if process == 4:
            user.admin = True

        db.session.merge(user)
        db.session.commit()
    
    def delete_privilege(user, process):

        user = db.session.get(User, user)

        if process == 1:
            user.edit = False
        if process == 2:
            user.check = False
        if process == 3:
            user.approve = False
        if process == 4:
            user.admin = False

        db.session.merge(user)
        db.session.commit()

    def register_process():

        processes = ['編集', '確認', '承認', '管理']
        for process in processes:
            process = Process(
                process = process
            )
            db.session.add(process)

        db.session.commit()


class ScoreManager:

    def add_score(user, question, correct, review):
        new_score = Score(
            user = user,
            question =  question,
            correct = correct,
            review = review,
            answered_at = datetime.now()
        )

        db.session.add(new_score)
        db.session.commit()

    def culculate_ratio_each_grade(user):
        grades = Grade.query.order_by(Grade.id.asc()).all()
        grades_info = []
        for grade in grades:
            question_count = Question.query.join(Element).join(E_Group).filter(E_Group.grade==grade.id).count()
            answered_count_all = Score.query.with_entities(Score.question).filter(Score.user==user).group_by(Score.question)
            answered_count = Question.query.join(Element).join(E_Group).filter(E_Group.grade==grade.id).filter(Question.id.in_(answered_count_all)).count()

            if answered_count==0 or question_count==0:
                grade_ratio = {
                    'id': grade.id,
                    'grade': grade.grade,
                    'ratio': 0
                }
            else:
                grade_ratio = {
                    'id': grade.id,
                    'grade': grade.grade,
                    'ratio': '{:.0%}'.format(answered_count/question_count)
                }
            grades_info.append(grade_ratio)

        return grades_info
        
