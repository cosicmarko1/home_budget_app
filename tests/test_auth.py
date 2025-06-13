from app.main import app
from tests.helpers import client, generate_random_username, register_user, login_user


def test_register_user():
    username = generate_random_username()
    response = register_user(username)
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_register_existing_user():
    username = generate_random_username()
    register_user(username)
    response = register_user(username)
    assert response.status_code == 400


def test_login_valid_credentials():
    username = generate_random_username()
    password = "testpass12"
    register_user(username, password)
    response = login_user(username, password)
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_invalid_credentials():
    response = login_user("invaliduser", "invalidpass")
    assert response.status_code == 401
