import environments
from app import models
from sqlalchemy.orm import Session


def create_default_categories(db: Session, user_id: int):
    for name in environments.DEFAULT_CATEGORIES:
        db.add(models.Category(name=name, owner_id=user_id))
    db.commit()
