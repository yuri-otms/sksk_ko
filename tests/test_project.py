from sksk_app.models.questions import User

def test_home(client):
    response = client.get("/")
    assert b"<title>" in response.data


def test_signup_post(client, app):
    response = client.post("/signup", data={"name": "test2", "email": "test2@test.com", "password": "1234"})

    with app.app_context():
        assert User.query.count() == 4
        assert User.query.first().email == "test2@test.com"

