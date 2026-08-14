from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.users import schemas
from app.users.repository import UserRepository

class UserService:
    def __init__(self):
        self.repository = UserRepository()

    def get_users(self, db: Session, skip: int = 0, limit: int = 10):
        return self.repository.get_all(db, skip=skip, limit=limit)

    def get_user(self, db: Session, user_id: int):
        user = self.repository.get_by_id(db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="User not found"
            )
        return user

    def create_user(self, db: Session, user: schemas.UserCreate):
        db_user = self.repository.get_by_email(db, email=user.email)
        if db_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Email already registered"
            )
        return self.repository.create(db=db, user=user)

    def update_user(self, db: Session, user_id: int, user_update: schemas.UserUpdate):
        db_user = self.get_user(db, user_id)
        
        if user_update.email and user_update.email != db_user.email:
            existing_user = self.repository.get_by_email(db, email=user_update.email)
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, 
                    detail="Email already registered"
                )
                
        return self.repository.update(db, db_user, user_update)

    def delete_user(self, db: Session, user_id: int):
        db_user = self.get_user(db, user_id)
        self.repository.delete(db, db_user)
        return {"message": "User deleted successfully"}
