from sqlalchemy.orm import Session
from app.users import models, schemas

class UserRepository:
    def get_all(self, db: Session, skip: int = 0, limit: int = 10):
        return db.query(models.User).offset(skip).limit(limit).all()

    def get_by_id(self, db: Session, user_id: int):
        return db.query(models.User).filter(models.User.id == user_id).first()

    def get_by_email(self, db: Session, email: str):
        return db.query(models.User).filter(models.User.email == email).first()

    def create(self, db: Session, user: schemas.UserCreate):
        db_user = models.User(
            name=user.name, 
            email=user.email, 
            age=user.age
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    def update(self, db: Session, db_user: models.User, user_update: schemas.UserUpdate):
        update_data = user_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_user, key, value)
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    def delete(self, db: Session, db_user: models.User):
        db.delete(db_user)
        db.commit()
        return True
