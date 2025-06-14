from pydantic import BaseModel


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
