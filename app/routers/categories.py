from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db
from app.auth import get_current_user

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.post("/", response_model=schemas.Category)
def create_category(
    category: schemas.CategoryCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    new_category = models.Category(name=category.name, owner_id=current_user.id)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category


@router.get("/", response_model=list[schemas.Category])
def get_categories(
    db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)
):
    return (
        db.query(models.Category)
        .filter(models.Category.owner_id == current_user.id)
        .all()
    )


@router.delete("/{category_id}", status_code=204)
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    category = (
        db.query(models.Category)
        .filter_by(id=category_id, owner_id=current_user.id)
        .first()
    )
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    db.delete(category)
    db.commit()
