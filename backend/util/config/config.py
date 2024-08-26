from typing import List
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # BACKEND_CORS_ORIGINS: List[str]
    DB_CONFIG: str
    
    class Config:
        env_file = ".env"

settings = Settings()