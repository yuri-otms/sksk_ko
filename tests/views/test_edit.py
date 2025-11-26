from flask import session
from sqlalchemy import func

from app import db
from app.models import Grade

def test_show(client, app, auth):
    auth.login()
    response = client.get('/edit/show/elements?g=1')
    assert response.status_code == 200

    with app.app_context():
        grade = db.session.query(Grade).all()
        assert grade is not None


    

