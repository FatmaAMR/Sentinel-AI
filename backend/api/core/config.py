"""
CORE In general for System Configuration 
It manages Environment Variables (.env), API keys, and global Project Constants.


Team Note: Use Pydantic Settings here to ensure the app fails fast if the HF_TOKEN is missing.

"""
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Sentinel AI"
    API_V1_STR: str = "/api/v1"
    HF_TOKEN: str
    DATABASE_URL: str = "sqlite:///./sentinel.db"

    class Config:
        env_file = ".env"

settings = Settings()