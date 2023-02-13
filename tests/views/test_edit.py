from flask import session
from sqlalchemy import func

from sksk_app import db
from sksk_app.models import Level

def test_show(client, app, auth):
    auth.login()
    response = client.get('/edit/show')
    assert response.status_code == 200
    assert b"edit_toppage" in response.data

    with app.app_context():
        level = db.session.query(Level).all()
        assert level is not None

def test_add_level(client, app, auth):
    auth.login()
    response = client.post(
    '/edit/add/level', data={'level_name':'ハン検1級', 'level_desc':'ハン検1級の内容'})
    assert response.headers["Location"] == "/edit/add/level/done"

    with app.app_context():
        max_position = db.session.query(
            func.max(Level.position).label('level_max')).one()
        max = int(max_position.level_max)
        assert max is not None

    

