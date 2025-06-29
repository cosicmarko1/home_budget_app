from app.main import app
from fastapi.testclient import TestClient
from tests.helpers import get_auth_header, create_category, create_expense

client = TestClient(app)


def test_create_expense():
    headers = get_auth_header()
    category_response = client.post(
        "/categories/", json={"name": "Utilities"}, headers=headers
    )
    category_id = category_response.json()["id"]

    expense_data = {
        "amount": 50.0,
        "description": "Electricity bill",
        "category_id": category_id,
    }
    response = client.post("/expenses/", json=expense_data, headers=headers)

    assert response.status_code == 200
    json_data = response.json()
    assert json_data["amount"] == 50.0
    assert json_data["description"] == "Electricity bill"
    assert json_data["category_id"] == category_id


def test_get_expenses():
    headers = get_auth_header()
    category_response = client.post(
        "/categories/", json={"name": "Groceries"}, headers=headers
    )
    category_id = category_response.json()["id"]
    client.post(
        "/expenses/",
        json={"amount": 30.0, "description": "Groceries", "category_id": category_id},
        headers=headers,
    )

    response = client.get("/expenses/", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0


def test_delete_expense():
    headers = get_auth_header()
    category_response = client.post(
        "/categories/", json={"name": "Transport"}, headers=headers
    )
    category_id = category_response.json()["id"]

    expense_response = client.post(
        "/expenses/",
        json={"amount": 10.0, "description": "Bus ticket", "category_id": category_id},
        headers=headers,
    )
    expense_id = expense_response.json()["id"]

    delete_response = client.delete(f"/expenses/{expense_id}", headers=headers)
    assert delete_response.status_code == 204

    response = client.get("/expenses/", headers=headers)
    assert all(exp["id"] != expense_id for exp in response.json())


def test_create_expenses_with_different_payment_methods():
    headers = get_auth_header()
    category = create_category(headers, "Payment Test")

    e1 = create_expense(headers, 50.0, category["id"], payment_method="cash")
    assert e1["payment_method"] == "cash"

    e2 = create_expense(headers, 75.0, category["id"], payment_method="card")
    assert e2["payment_method"] == "card"

    e3 = create_expense(headers, 120.0, category["id"], payment_method="bank transfer")
    assert e3["payment_method"] == "bank transfer"
