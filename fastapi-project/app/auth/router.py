from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.auth import schemas
from app.auth.service import AuthService
from app.auth.dependencies import get_current_user
from app.users import models

router = APIRouter(prefix="/auth")
auth_service = AuthService()

# --- Account ---
@router.post("/register", tags=["(Auth) Account"])
async def register(data: schemas.RegisterUser, db: Session = Depends(get_db)):
    return await auth_service.register_user(db, data)

@router.post("/login", tags=["(Auth) Account"])
async def login(data: schemas.LoginUser, db: Session = Depends(get_db)):
    return await auth_service.login_user(db, data)

@router.post("/refresh-token", tags=["(Auth) Account"], response_model=schemas.TokenResponse)
def refresh_token(data: schemas.RefreshToken, db: Session = Depends(get_db)):
    return auth_service.refresh_token(db, data)

# --- OTP ---
@router.post("/resend-otp", tags=["(Auth) OTP"])
async def resend_otp(data: schemas.ResendOTP, db: Session = Depends(get_db)):
    return await auth_service.resend_otp(db, data)

@router.post("/verify-otp", tags=["(Auth) OTP"])
def verify_otp(data: schemas.VerifyOTP, db: Session = Depends(get_db)):
    return auth_service.verify_otp(db, data)

# --- Password ---
@router.post("/forgot-password", tags=["(Auth) Password"])
async def forgot_password(data: schemas.ForgotPassword, db: Session = Depends(get_db)):
    return await auth_service.forgot_password(db, data)

@router.post("/reset-password", tags=["(Auth) Password"])
def reset_password(data: schemas.ResetPassword, db: Session = Depends(get_db)):
    return auth_service.reset_password(db, data)

@router.post("/change-password", tags=["(Auth) Password"])
def change_password(data: schemas.ChangePassword, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return auth_service.change_password(db, current_user, data)
