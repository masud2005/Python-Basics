from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime, timedelta
import uuid

from app.users import models
from app.auth import schemas, utils

class AuthService:
    def _create_otp_challenge(self, db: Session, email: str, purpose: str) -> str:
        challenge_id = str(uuid.uuid4())
        otp = utils.generate_otp()
        
        # Invalidate old challenges for this email and purpose
        db.query(models.OTPChallenge).filter(
            models.OTPChallenge.email == email,
            models.OTPChallenge.purpose == purpose
        ).delete()
        
        challenge = models.OTPChallenge(
            challenge_id=challenge_id,
            email=email,
            otp_code=otp,
            purpose=purpose,
            expires_at=datetime.utcnow() + timedelta(minutes=10)
        )
        db.add(challenge)
        db.commit()
        return challenge_id, otp

    async def register_user(self, db: Session, user: schemas.RegisterUser):
        existing_user = db.query(models.User).filter(models.User.email == user.email).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
            
        # Create unverified user
        db_user = models.User(
            name=user.name,
            email=user.email,
            hashed_password=utils.get_password_hash(user.password),
            is_verified=False
        )
        db.add(db_user)
        db.commit()
        
        # Create OTP challenge
        challenge_id, otp = self._create_otp_challenge(db, user.email, "register")
        await utils.send_otp_email(user.email, otp, "Registration Verification")
        
        return schemas.ChallengeResponse(
            challenge_id=challenge_id, 
            message="OTP sent to your email to verify account."
        )

    async def login_user(self, db: Session, credentials: schemas.LoginUser):
        user = db.query(models.User).filter(models.User.email == credentials.email).first()
        if not user or not utils.verify_password(credentials.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid credentials")
            
        if not user.is_verified:
            # Resend verification OTP if not verified
            challenge_id, otp = self._create_otp_challenge(db, user.email, "register")
            await utils.send_otp_email(user.email, otp, "Registration Verification")
            return schemas.ChallengeResponse(
                challenge_id=challenge_id, 
                message="Account not verified. New OTP sent to email."
            )
            
        # Optional: Direct login or Login OTP. Let's do direct login as standard, returning tokens.
        access_token = utils.create_access_token(data={"sub": user.email})
        refresh_token = utils.create_refresh_token(data={"sub": user.email})
        
        return schemas.TokenResponse(access_token=access_token, refresh_token=refresh_token)

    def refresh_token(self, db: Session, token_data: schemas.RefreshToken):
        try:
            payload = jwt.decode(token_data.refresh_token, settings.JWT_REFRESH_SECRET, algorithms=[settings.ALGORITHM])
            email = payload.get("sub")
            if not email:
                raise HTTPException(status_code=401, detail="Invalid refresh token")
                
            user = db.query(models.User).filter(models.User.email == email).first()
            if not user:
                raise HTTPException(status_code=401, detail="Invalid user")
                
            access_token = utils.create_access_token(data={"sub": user.email})
            new_refresh_token = utils.create_refresh_token(data={"sub": user.email})
            
            return schemas.TokenResponse(access_token=access_token, refresh_token=new_refresh_token)
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid or expired refresh token")

    async def resend_otp(self, db: Session, data: schemas.ResendOTP):
        old_challenge = db.query(models.OTPChallenge).filter(models.OTPChallenge.challenge_id == data.challenge_id).first()
        if not old_challenge:
            raise HTTPException(status_code=404, detail="Challenge not found")
            
        challenge_id, otp = self._create_otp_challenge(db, old_challenge.email, old_challenge.purpose)
        await utils.send_otp_email(old_challenge.email, otp, f"{old_challenge.purpose} verification")
        
        return schemas.ChallengeResponse(challenge_id=challenge_id, message="OTP resent successfully.")

    def verify_otp(self, db: Session, data: schemas.VerifyOTP):
        challenge = db.query(models.OTPChallenge).filter(
            models.OTPChallenge.challenge_id == data.challenge_id,
            models.OTPChallenge.otp_code == data.otp_code
        ).first()
        
        if not challenge:
            raise HTTPException(status_code=400, detail="Invalid OTP")
        if challenge.expires_at < datetime.utcnow():
            raise HTTPException(status_code=400, detail="OTP expired")
            
        challenge.is_verified = True
        db.commit()
        
        # If it was a registration, verify the user
        if challenge.purpose == "register":
            user = db.query(models.User).filter(models.User.email == challenge.email).first()
            if user:
                user.is_verified = True
                db.commit()
                # Auto login after verification
                access_token = utils.create_access_token(data={"sub": user.email})
                refresh_token = utils.create_refresh_token(data={"sub": user.email})
                return schemas.TokenResponse(access_token=access_token, refresh_token=refresh_token)
                
        return {"message": "OTP verified successfully. You can proceed."}

    async def forgot_password(self, db: Session, data: schemas.ForgotPassword):
        user = db.query(models.User).filter(models.User.email == data.email).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
            
        challenge_id, otp = self._create_otp_challenge(db, user.email, "reset_password")
        await utils.send_otp_email(user.email, otp, "Password Reset")
        
        return schemas.ChallengeResponse(challenge_id=challenge_id, message="OTP sent to email for password reset.")

    def reset_password(self, db: Session, data: schemas.ResetPassword):
        challenge = db.query(models.OTPChallenge).filter(models.OTPChallenge.challenge_id == data.challenge_id).first()
        if not challenge or not challenge.is_verified or challenge.purpose != "reset_password":
            raise HTTPException(status_code=400, detail="OTP not verified or invalid challenge")
            
        user = db.query(models.User).filter(models.User.email == challenge.email).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
            
        user.hashed_password = utils.get_password_hash(data.new_password)
        db.delete(challenge) # Cleanup
        db.commit()
        
        return {"message": "Password reset successfully."}

    def change_password(self, db: Session, current_user: models.User, data: schemas.ChangePassword):
        if not utils.verify_password(data.old_password, current_user.hashed_password):
            raise HTTPException(status_code=400, detail="Invalid old password")
            
        current_user.hashed_password = utils.get_password_hash(data.new_password)
        db.commit()
        return {"message": "Password changed successfully."}
