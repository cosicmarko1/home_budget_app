from datetime import date
from tests.helpers import (
    client,
    generate_random_username,
    register_user,
    login_user,
    create_category,
    create_expense,
)


def auth_headers():
    username = generate_random_username()
    password = "testpass123"
    register_user(username, password)
    token_response = login_user(username, password)
    access_token = token_response.json()["access_token"]
    return {"Authorization": f"Bearer {access_token}"}


def test_filter_expenses_by_amount_range():
    headers = auth_headers()
    category = create_category(headers, "Utilities")

    exp1 = create_expense(headers, 20, category["id"])
    exp2 = create_expense(headers, 60, category["id"])
    exp3 = create_expense(headers, 100, category["id"])

    response = client.get("/expenses/?min_amount=30&max_amount=80", headers=headers)
    assert response.status_code == 200
    result_ids = {e["id"] for e in response.json()}
    expected_ids = {exp2["id"]}

    assert expected_ids.issubset(result_ids)


def test_filter_expenses_by_date_range():
    headers = auth_headers()
    category = create_category(headers, "Transport")

    create_expense(headers, 40, category["id"], date="2024-01-01")
    exp2 = create_expense(headers, 80, category["id"], date="2024-02-01")

    response = client.get(
        "/expenses/?start_date=2024-01-15&end_date=2024-02-15", headers=headers
    )
    assert response.status_code == 200
    result_ids = {e["id"] for e in response.json()}
    assert exp2["id"] in result_ids


def test_combined_filters():
    headers = auth_headers()
    category = create_category(headers, "Dining")

    create_expense(headers, 15, category["id"], date="2024-01-01")
    match = create_expense(headers, 45, category["id"], date="2024-02-01")

    response = client.get(
        f"/expenses/?category_id={category['id']}&min_amount=40&max_amount=50&start_date=2024-01-15&end_date=2024-02-28",
        headers=headers,
    )
    assert response.status_code == 200
    results = response.json()

    result_ids = {e["id"] for e in results}
    assert match["id"] in result_ids
