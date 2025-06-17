from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db
from app.auth import get_current_user
from typing import Optional, List
from datetime import date, timedelta
from sqlalchemy import func

router = APIRouter(prefix="/expenses", tags=["expenses"])


@router.post("/", response_model=schemas.ExpenseResponse)
def create_expense(
    expense: schemas.ExpenseCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    db_category = (
        db.query(models.Category)
        .filter_by(id=expense.category_id, owner_id=current_user.id)
        .first()
    )

    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")

    new_expense = models.Expense(
        amount=expense.amount,
        description=expense.description,
        user_id=current_user.id,
        category_id=expense.category_id,
    )
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    return new_expense


@router.get("/", response_model=list[schemas.ExpenseResponse])
def get_expenses(
    db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)
):
    return db.query(models.Expense).filter_by(user_id=current_user.id).all()


@router.delete("/{expense_id}", status_code=204)
def delete_expense(
    expense_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    expense = (
        db.query(models.Expense)
        .filter_by(id=expense_id, user_id=current_user.id)
        .first()
    )

    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    db.delete(expense)
    db.commit()


@router.get("/filter/", response_model=List[schemas.ExpenseResponse])
def filter_expenses(
    category_id: Optional[int] = Query(None),
    min_amount: Optional[float] = Query(None),
    max_amount: Optional[float] = Query(None),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    description: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    query = db.query(models.Expense).filter(models.Expense.user_id == current_user.id)

    if category_id is not None:
        query = query.filter(models.Expense.category_id == category_id)
    if min_amount is not None:
        query = query.filter(models.Expense.amount >= min_amount)
    if max_amount is not None:
        query = query.filter(models.Expense.amount <= max_amount)
    if start_date is not None:
        query = query.filter(models.Expense.date >= start_date)
    if end_date is not None:
        query = query.filter(models.Expense.date <= end_date)
    if description is not None:
        query = query.filter(models.Expense.description.ilike(f"%{description}%"))

    return query.order_by(models.Expense.date.desc()).all()


@router.get("/summary/", response_model=schemas.ExpenseSummaryResponse)
def get_expense_summary(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    today = date.today()

    # time ranges and labels
    periods = {
        "last_7_days": 7,
        "last_month": 30,
        "last_3_months": 90,
        "last_year": 365,
    }

    summary = {
        label: float(
            db.query(func.sum(models.Expense.amount))
            .filter(
                models.Expense.user_id == current_user.id,
                models.Expense.date >= today - timedelta(days=days),
            )
            .scalar()
            or 0.0
        )
        for label, days in periods.items()
    }

    return summary
