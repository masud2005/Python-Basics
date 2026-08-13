
# pyrefly: ignore [missing-import]
from fastapi import FastAPI
# pyrefly: ignore [missing-import]
from pydantic import BaseModel
from routers import users

class User(BaseModel):
    name: str
    email: str
    age: int
    is_active: bool = True
    is_verified: bool = False

app = FastAPI()

app.include_router(users.router)

@app.get("/")
def root():
    return {"message": "Hello FastAPI! I am ready."}

@app.get("/hello/{name}")
def say_hello(name: str):
    return {"message": f"Hello {name}, Welcome to FastAPI!"}

@app.get("/items")
def read_items(skip: int = 0, limit: int = 10):
    return {"message": f"Showing {limit} items starting from {skip}"}

@app.post("/create-user")
def create_user(user: User):
    return {
        "message": "User created successfully!",
        "data": user
    }