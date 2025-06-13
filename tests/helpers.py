import uuid
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def generate_random_username(prefix="user"):
    return f"{prefix}_{uuid.uuid4().hex[:6]}"


def register_user(username: str, password: str = "defaultpass"):
    response = client.post(
        "/register", json={"username": username, "password": password}
    )
    return response


def login_user(username: str, password: str = "default_pass"):
    response = client.post("/login", data={"username": username, "password": password})
    return response
