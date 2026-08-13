# pyrefly: ignore [missing-import]
from fastapi import FastAPI, HTTPException
# pyrefly: ignore [missing-import]
from pydantic import BaseModel
from typing import Optional
# pyrefly: ignore [missing-import]
from fastapi import APIRouter

router = APIRouter()

fake_db = {
    1: {"name": "Masud", "email": "masud@example.com"},
    2: {"name": "Rahim", "email": "rahim@example.com"}
}

class User(BaseModel):
    name: str
    email: str

class UpdateUser(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None

@router.get("/users")
def get_all_users():
    return {
        "message": "All Users Retrieved Successfully.",
        "data": fake_db
    }

@router.get("/users/{user_id}")
def get_user(user_id):
    if(user_id not in fake_db):
        raise HTTPException(status_code=404, detail= "User Not Found!")
    return {
        "message": "User Retrieved Successfully!",
        "data": fake_db.get(user_id)
    }

@router.post("/create-user")
def create_user(user: User):
    new_id = max(fake_db.keys()) + 1
    fake_db[new_id] = user.dict()
    return {
        "message": "User Created Successfully!",
        "data": fake_db[new_id]
    }

@router.patch("/users/{user_id}")
def update_user(user_id, user: UpdateUser):
    if(user_id not in fake_db):
        raise HTTPException(status_code=404, detail= "User Not Found!")
    
    # Update only the fields that are provided
    if user.name:
        fake_db[user_id]['name'] = user.name
    if user.email:
        fake_db[user_id]['email'] = user.email
    
    return {
        "message": "User Updated Successfully!",
        "data": fake_db[user_id]
    }


@router.delete("/users/{user_id}")
def delete_user(user_id):
    if(user_id not in fake_db):
        raise HTTPException(status_code=404, detail= "User Not Found!")
    del fake_db[user_id]
    return {
        "message": "User Deleted Successfully!"
    }
