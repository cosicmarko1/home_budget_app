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


def create_category(headers, name):
    response = client.post("/categories/", json={"name": name}, headers=headers)
    return response.json()


def create_expense(
    headers,
    amount: float,
    category_id: int,
    date: str = None,
    payment_method: str = "cash",
):
    data = {
        "amount": amount,
        "category_id": category_id,
        "payment_method": payment_method,
    }
    if date:
        data["date"] = date

    response = client.post("/expenses/", headers=headers, json=data)

    if response.status_code != 200:
        print("Failed to create expense.")
        print("Request data:", data)
        print("Response status code:", response.status_code)
        print("Response JSON:", response.json())

    assert response.status_code == 200, response.json()
    return response.json()
