from sksk_app.models.questions import User

# def test_signup_post(client, app):
#     response = client.post("/signup", data={"name": "test2", "email": "test2@test.com", "password": "1234"})

#     with app.app_context():
#         assert User.query.first().email == "test2@test.com"

def test_signup_post(client):
    client.get('/signup_done')
    with client.session_transaction() as session:
        flash_message = dict(session["_flashes"]).get('message')

    assert "ユーザー登録を行いました。" == flash_message