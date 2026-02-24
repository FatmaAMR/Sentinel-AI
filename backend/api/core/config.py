import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from typing import List

ENV_FILE_PATH = Path("/mnt/d/AI Career/GP/Sentinel/backend/.env")

class Settings(BaseSettings):
    APP_NAME: str = "Sentinel"
    APP_VESRION: str = "0.1"
    
    FILE_ALLOWED_TYPES: List[str] = ["pdf", "docx", "txt", "rtf"]
    FILE_MAX_SIZE: int = 10
    
    GROQ_API_KEY: str  
    GROQ_MODEL_NAME: str = "llama-3.1-8b-instant"
    
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE_PATH), 
        extra="ignore"
    )

@lru_cache()
def get_settings():
    if not ENV_FILE_PATH.exists():
        
        print(f"Warning: .env file NOT FOUND at {ENV_FILE_PATH}")
    
    s = Settings()
    s.DATABASE_URL = s.DATABASE_URL.strip()
    #print(f"DEBUG: Connecting to DB -> {s.DATABASE_URL}")
    return s

settings = get_settings()