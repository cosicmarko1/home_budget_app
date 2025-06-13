from sqlalchemy import Column, Integer, String, Float
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=True)
    hashed_password = Column(String(128), nullable=False)
    balance = Column(Float, default=1000.0)
