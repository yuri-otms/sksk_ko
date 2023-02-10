from flask import session, g
from sksk_app.models.questions import User

# def test_signup_post(client, app):
#     response = client.post('/signup', data={"name": "test2", "email": "test2@test.com", "password": "1234"})

#     with app.app_context():
#         assert User.query.first().email == "test2@test.com"

# def test_signup_post(client):
#     client.get('/signup_done')
#     with client.session_transaction() as session:
#         flash_message = dict(session["_flashes"]).get('message')

#     assert "ユーザー登録を行いました。" == flash_message

def test_signup_post(client, app):
    assert client.get('/auth/signup').status_code == 200
    response = client.post(
        '/auth/signup', data={'name':'testA','email': 'testA@test.com', 'password': '1234'}
    )
    assert response.headers["Location"] == "/auth/signup"

    with app.app_context():
        user = User.query.filter_by(email='testA@test.com').first()
        assert user is not None

def test_login(client, auth):
    assert client.get('/auth/login').status_code == 200
    response = auth.login()
    assert response.headers["Location"] == "/"

    with client:
        client.get('/')
        assert session['user_id'] == 4
        assert g.user['name'] == 'test'

def test_logout(client, auth):
    auth.login()

    with client:
        auth.logout()
        assert 'user_id' not in session