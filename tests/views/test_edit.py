from flask import session
from sqlalchemy import func

from sksk_app.models import db,Level

def test_show(client, app):
    response = client.get('/edit/show')
    assert response.status_code == 200
    assert b"edit_toppage" in response.data

    with app.app_context():
        level = db.session.query(Level).all()
        assert level is not None

def test_add_level(client, app):
    response = client.post(
    '/edit/add/level', data={'level_name':'ハン検1級', 'level_desc':'ハン検1級の内容'})

    with app.app_context():
        max_position = db.session.query(
            func.max(Level.position).label('level_max')).one()
        max = int(max_position.level_max)
        assert max is not None

    

