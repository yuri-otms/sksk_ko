from flask import session
from sqlalchemy import func

from sksk_app import db
from sksk_app.models import Level

def test_show(client, app, auth):
    auth.login()
    response = client.get('/edit/show?g=1')
    assert response.status_code == 200
    assert b"edit_toppage" in response.data

    with app.app_context():
        level = db.session.query(Level).all()
        assert level is not None


    

