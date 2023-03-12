from flask import session
from sksk_app.models import db, User, Grade

# def test_signup_post(client, app):
#     assert client.get('/auth/signup').status_code == 200
    
#     response = client.post(
#         '/auth/signup', data={'name':'test','email': 'test@test.com', 'password': '1234'}
#     )
#     assert response.headers["Location"] == "/auth/signup"

#     with app.app_context():
#         user = User.query.filter_by(email='test@test.com').first()
#         assert user is not None

# def test_login(client, auth):
#     assert client.get('/auth/login').status_code == 200
#     response = auth.login()
#     assert response.headers["Location"] == "/question/check_login"

#     with client:
#         client.get('/')
#         assert session['user_id'] == 1
#         assert g.user['name'] == 'test'

def test_logout(client, auth):
    auth.login()

    with client:
        auth.logout()
        assert 'user_id' not in session