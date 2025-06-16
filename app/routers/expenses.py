from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db
from app.auth import get_current_user

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
