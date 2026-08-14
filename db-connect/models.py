# pyrefly: ignore [missing-import]
from sqlalchemy import Column, Integer, String, Boolean
# pyrefly: ignore [missing-import]
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, index=True)
    age = Column(Integer)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)