from sksk_app import db
from sksk_app.models import Level


class QuestionManager:
    def delete_testing_levels():

        levels = Level.query.filter(Level.id.between(10, 200)).delete()
        db.session.commit()