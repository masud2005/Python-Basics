from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    
    # JWT Config
    JWT_ACCESS_SECRET: str
    JWT_REFRESH_SECRET: str
    ACCESS_TOKEN_EXPIRES_IN: int = 15
    REFRESH_TOKEN_EXPIRES_IN: int = 43200
    ALGORITHM: str = "HS256"

    # SMTP Config
    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASS: str
    SMTP_FROM: str
    
    class Config:
        env_file = ".env"

settings = Settings()
