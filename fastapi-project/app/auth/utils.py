import bcrypt
from jose import jwt
from datetime import datetime, timedelta
import random
import string
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema

from app.core.config import settings

# --- Password Hashing ---
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def get_password_hash(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

# --- JWT Tokens ---
def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRES_IN)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.JWT_ACCESS_SECRET, algorithm=settings.ALGORITHM)

def create_refresh_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRES_IN)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.JWT_REFRESH_SECRET, algorithm=settings.ALGORITHM)

# --- OTP Generation ---
def generate_otp(length: int = 6) -> str:
    return ''.join(random.choices(string.digits, k=length))

# --- Email Service ---
mail_conf = ConnectionConfig(
    MAIL_USERNAME=settings.SMTP_USER,
    MAIL_PASSWORD=settings.SMTP_PASS,
    MAIL_FROM=settings.SMTP_USER,
    MAIL_PORT=settings.SMTP_PORT,
    MAIL_SERVER=settings.SMTP_HOST,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True
)

async def send_otp_email(email: str, otp: str, purpose: str):
    message = MessageSchema(
        subject=f"Your OTP for {purpose}",
        recipients=[email],
        body=f"Your One-Time Password is: {otp}. It expires in 10 minutes.",
        subtype="plain"
    )
    fm = FastMail(mail_conf)
    try:
        await fm.send_message(message)
    except Exception as e:
        print(f"Error sending email: {e}")
        pass
