from fastapi import FastAPI
from app.routers import users, categories, expenses
from app.database import Base, engine
from app.models import User

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(users.router)
app.include_router(categories.router)
app.include_router(expenses.router)


@app.get("/")
def read_root():
    return {"message": "Home Budget API is now running"}
