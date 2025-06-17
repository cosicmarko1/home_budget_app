from pydantic import BaseModel
from typing import Optional
from datetime import date


class UserCreate(BaseModel):
    username: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    balance: float

    class Config:
        model_config = {"from_attributes": True}


class Token(BaseModel):
    access_token: str
    token_type: str


class CategoryBase(BaseModel):
    name: str


class CategoryCreate(CategoryBase):
    pass


class Category(CategoryBase):
    id: int

    class Config:
        model_config = {"from_attributes": True}


class ExpenseBase(BaseModel):
    amount: float
    description: Optional[str] = None
    category_id: int


class ExpenseCreate(ExpenseBase):
    pass


class ExpenseResponse(ExpenseBase):
    id: int
    amount: float
    description: Optional[str]
    date: Optional[date]
    category_id: int

    class Config:
        from_attributes = True


class ExpenseSummaryResponse(BaseModel):
    last_7_days: float
    last_month: float
    last_3_months: float
    last_year: float
