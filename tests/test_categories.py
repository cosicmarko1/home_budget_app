from tests.helpers import client, get_auth_header


def test_create_category():
    headers = get_auth_header()
    response = client.post("/categories/", json={"name": "Groceries"}, headers=headers)
    assert response.status_code == 200
    assert response.json()["name"] == "Groceries"


def test_get_categories():
    headers = get_auth_header()
    client.post("/categories/", json={"name": "Bills"}, headers=headers)
    client.post("/categories/", json={"name": "Entertainment"}, headers=headers)

    response = client.get("/categories/", headers=headers)
    assert response.status_code == 200
    names = [cat["name"] for cat in response.json()]
    assert "Bills" in names
    assert "Entertainment" in names


def test_delete_category():
    headers = get_auth_header()
    create = client.post("/categories/", json={"name": "Temporary"}, headers=headers)
    category_id = create.json()["id"]

    response = client.delete(f"/categories/{category_id}", headers=headers)
    assert response.status_code == 204

    list_response = client.get("/categories/", headers=headers)
    assert category_id not in [cat["id"] for cat in list_response.json()]


def test_unauthorized_access_blocked():
    response = client.get("/categories/")
    assert response.status_code == 401
