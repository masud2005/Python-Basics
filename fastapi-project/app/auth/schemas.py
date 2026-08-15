from pydantic import BaseModel, EmailStr
from typing import Optional

# --- Account Schemas ---
class RegisterUser(BaseModel):
    name: str
    email: EmailStr
    password: str

class LoginUser(BaseModel):
    email: EmailStr
    password: str

class RefreshToken(BaseModel):
    refresh_token: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class ChallengeResponse(BaseModel):
    challenge_id: str
    message: str

# --- OTP Schemas ---
class VerifyOTP(BaseModel):
    challenge_id: str
    otp_code: str

class ResendOTP(BaseModel):
    challenge_id: str

# --- Password Schemas ---
class ForgotPassword(BaseModel):
    email: EmailStr

class ResetPassword(BaseModel):
    challenge_id: str
    new_password: str

class ChangePassword(BaseModel):
    old_password: str
    new_password: str
