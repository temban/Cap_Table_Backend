import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()

DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:admin@localhost:5432/cap_table_db")
SECRET_KEY: str = os.getenv("SECRET_KEY", "EWERSDFSFSFSDFSDFSDFT5QT5")
ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
REFRESH_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES", 60 * 24 * 7))

class Settings(BaseSettings):
    # Email configuration
    COMPANY_NAME: str = os.getenv("COMPANY_NAME", "Cap Table Management")
    SMTP_HOST: str = os.getenv("SMTP_HOST", "smtp.gmail.com")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", 587))
    SMTP_USER: str = os.getenv("SMTP_USER", "tembanblaise12@gmail.com")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASS", "srlc cxsg jwqy bfqw")
    SMTP_FROM: str = os.getenv("SMTP_FROM", "tembanblaise12@gmail.com")
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")

    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()