from flask import session

from sksk_app import db
from sksk_app.models import User, Level

def test_index(client):
    assert client.get('/').status_code == 200

def test_user(app):
    with app.app_context():
        user = User.query.all()
        assert user is not None

def test_add_privilege(client, auth):
    auth.login()
    response = client.get('/admin/add_privilege?user_id=2&process_id=2')
    assert response.status_code == 200

# def test_add_privilege_execute(client):
    # response = client.post('/admin/privilege_added', data={'user_id':2, 'processed_id':2})
    # assert response.headers["Location"] == '/admin/privilege_added'

def test_add_privilege_done(client):
    #リダイレクト
    assert client.get('/admin/privilege_added_done').status_code == 302

# def delete_privilege_execute(client):
    
def test_privilege_done(client):
    assert client.get('/admin/privilege_deleted_done').status_code == 302

