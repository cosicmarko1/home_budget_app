from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Home Budget API is now running"}