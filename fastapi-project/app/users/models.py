from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.core.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String) # For storing bcrypt hashed password
    age = Column(Integer, nullable=True)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)

class OTPChallenge(Base):
    __tablename__ = "otp_challenges"
    
    challenge_id = Column(String, primary_key=True, index=True)
    email = Column(String, index=True)
    otp_code = Column(String)
    purpose = Column(String) # login, register, reset_password
    expires_at = Column(DateTime)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
