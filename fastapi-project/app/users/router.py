from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.users import schemas
from app.users.service import UserService

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

user_service = UserService()

@router.post("/", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return user_service.create_user(db, user)

@router.get("/", response_model=List[schemas.UserResponse])
def get_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return user_service.get_users(db, skip=skip, limit=limit)

@router.get("/{user_id}", response_model=schemas.UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    return user_service.get_user(db, user_id)

@router.patch("/{user_id}", response_model=schemas.UserResponse)
def update_user(user_id: int, user_update: schemas.UserUpdate, db: Session = Depends(get_db)):
    return user_service.update_user(db, user_id, user_update)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user_service.delete_user(db, user_id)
    return None
