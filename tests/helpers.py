import uuid
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def generate_random_username(prefix="user"):
    return f"{prefix}_{uuid.uuid4().hex[:6]}"


def register_user(username: str, password: str = "defaultpass"):
    return client.post("/register", json={"username": username, "password": password})


def login_user(username: str, password: str = "default_pass"):
    return client.post("/login", data={"username": username, "password": password})


def get_auth_header(username=None, password="defaultpass"):
    username = username or generate_random_username()
    register_user(username, password)
    login_response = login_user(username, password)
    token = login_response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
