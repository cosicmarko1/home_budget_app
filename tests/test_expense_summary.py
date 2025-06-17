from datetime import date, timedelta
from app.database import SessionLocal
from app.models import Expense
from tests.helpers import client, get_auth_header, create_category, create_expense


def update_expense_date(expense_id: int, new_date: date):
    db = SessionLocal()
    try:
        expense = db.query(Expense).get(expense_id)
        expense.date = new_date
        db.commit()
    finally:
        db.close()


def test_expense_summary_aggregation():
    headers = get_auth_header()
    category = create_category(headers, "SummaryTest")
    today = date.today()

    # create expense and update date to last 7 days
    e1 = create_expense(headers, 100, category["id"])
    update_expense_date(e1["id"], today - timedelta(days=2))

    # create expense and update date to last 30 days
    e2 = create_expense(headers, 200, category["id"])
    update_expense_date(e2["id"], today - timedelta(days=10))

    # create expense and update date to last 3 months
    e3 = create_expense(headers, 300, category["id"])
    update_expense_date(e3["id"], today - timedelta(days=40))

    # create expense and update date to last year
    e4 = create_expense(headers, 400, category["id"])
    update_expense_date(e4["id"], today - timedelta(days=200))

    # create expense and update date to more than a year
    e5 = create_expense(headers, 500, category["id"])
    update_expense_date(e5["id"], today - timedelta(days=400))

    response = client.get("/expenses/summary/", headers=headers)
    assert response.status_code == 200
    summary = response.json()

    assert summary["last_7_days"] == 100.0
    assert summary["last_month"] == 300.0
    assert summary["last_3_months"] == 600.0
    assert summary["last_year"] == 1000.0
